import "dotenv/config";
import express from "express";
import { promises as fs } from "fs";
import { initSessionStore, newSession, lookupSession, successfulLogin, getUser } from "./session_store.js";
import bodyParser from "body-parser";
import cookieParser from "cookie-parser";
import { safeJson } from "./safe_fetch.js";
import { primeFlag } from "./prime_flag.js";
import { addUserTodo, deleteUserTodo, getUserTodos, initializeUserTodos, markUserTodoAsDone } from "./storage.js";

// https://stackoverflow.com/a/51391081
const asyncHandler = fn => (req, res, next) => {
    return Promise
        .resolve(fn(req, res, next))
        .catch(next);
};

await fs.mkdir(process.env.STORAGE_LOCATION, { recursive: true });
await initSessionStore();
await primeFlag();

const displayNamePreference = [
    "nickname",
    "preferred_username",
    "given_name",
    "name",
    "email",
    "sub"
]

const app = express();
app.use(bodyParser.urlencoded({
    limit: 8192,
    extended: false
}));
app.use(cookieParser());
app.set("view engine", "ejs"); // ejs on top

app.get("/", asyncHandler(async (req, res) => {
    if (!req.cookies.session) {
        return res.render("home.ejs", {
            base: process.env.BASE
        });
    }

    const userInfo = await getUser(req.cookies.session);
    if (!userInfo) {
        return res.render("home.ejs", {
            base: process.env.BASE
        });
    }

    const metadata = JSON.parse(userInfo.userMetadata);
    let name = "";
    for (let key of displayNamePreference) {
        if (metadata[key]) {
            name = metadata[key];
            break;
        }
    }

    await initializeUserTodos(userInfo.idpUrl, userInfo.userId);
    return res.render("todos.ejs", {
        name,
        todos: await getUserTodos(userInfo.idpUrl, userInfo.userId)
    });
}));

app.post("/start", asyncHandler(async (req, res) => {
    let response = null;
    try {
        response = await safeJson(req.body.issuer + "/.well-known/openid-configuration");
    } catch(e) {
    }
    if (response && response.issuer && response.authorization_endpoint && response.token_endpoint && response.userinfo_endpoint) {
        const session = await newSession(req.body.issuer, req.body.client_id);
        console.log(session);

        const search = new URLSearchParams();
        search.append("client_id", req.body.client_id);
        search.append("redirect_uri", process.env.BASE + "/auth_redirect");
        search.append("scope", "openid");
        search.append("response_type", "code");
        search.append("state", session);

        
        res.setHeader("Set-Cookie", `session=${session}; HttpOnly; Max-Age=3600; SameSite=Lax; Secure`);
        res.setHeader("Location", `${response.authorization_endpoint}?${search.toString()}`)
        res.sendStatus(302);
        
    } else {
        try {
            res.sendStatus(400);
            // res.write("Invalid OpenID configuration ;_;");
            res.end();
        } catch (ee) {
        }
    }
}));

app.post("/add", asyncHandler(async (req, res) => {
    if (!req.cookies.session) {
        return res.end("No auth");
    }

    const userInfo = await getUser(req.cookies.session);
    if (!userInfo) {
        return res.end("No auth");
    }

    if (!req.body.todo_name || req.body.todo_name > 256) return res.end("Todo too long");

    await addUserTodo(userInfo.idpUrl, userInfo.userId, req.body.todo_name);
    res.redirect("/");
}));

app.post("/done", asyncHandler(async (req, res) => {
    if (!req.cookies.session) {
        return res.end("No auth");
    }

    const userInfo = await getUser(req.cookies.session);
    if (!userInfo) {
        return res.end("No auth");
    }

    if (!req.body.todo_id) return res.end("No id");

    await markUserTodoAsDone(userInfo.idpUrl, userInfo.userId, req.body.todo_id);
    res.redirect("/");
}));

app.post("/delete", asyncHandler(async (req, res) => {
    if (!req.cookies.session) {
        return res.end("No auth");
    }

    const userInfo = await getUser(req.cookies.session);
    if (!userInfo) {
        return res.end("No auth");
    }

    if (!req.body.todo_id) return res.end("No id");

    await deleteUserTodo(userInfo.idpUrl, userInfo.userId, req.body.todo_id);
    res.redirect("/");
}));

app.get("/auth_redirect", asyncHandler(async (req, res) => {
    if (!req.cookies.session) return res.end("No session");
    if (req.cookies.session !== req.query.state) return res.end("Bad state");
    if (req.query.error) {
        return res.end("identity provider gave us an error.");
    }
    
    const sessionDetails = await lookupSession(req.cookies.session);
    const response = await safeJson(sessionDetails.idpUrl + "/.well-known/openid-configuration");
    if (!response.token_endpoint) return res.end("No token endpoint");
    if (!response.userinfo_endpoint) return res.end("No user info endpoint");

    const search = new URLSearchParams();
    search.append("grant_type", "authorization_code");
    search.append("code", req.query.code);
    search.append("redirect_uri", process.env.BASE + "/auth_redirect");
    search.append("client_id", sessionDetails.clientId);
    
    const tokenResponse = await safeJson(response.token_endpoint, {
        method: "POST",
        body: search.toString(),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    });

    if (!tokenResponse || !tokenResponse.access_token || !tokenResponse.token_type) return res.end("Bad token response");

    const userInfo = await safeJson(response.userinfo_endpoint, {
        headers: {
            "Authorization": `${tokenResponse.token_type} ${tokenResponse.access_token}`
        }
    });

    if (!userInfo || !userInfo.sub) return res.end("user has no sub");

    await successfulLogin(req.cookies.session, userInfo);
    res.setHeader("Location", `/`)
    res.sendStatus(302);
}));

app.listen(process.env.PORT || 2137);
