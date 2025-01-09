import path from "path";
import { createHash } from "crypto";
import { mkdirSync } from "fs";
import { createClient } from "@libsql/client";



function sha256sum(data) {
    return createHash("sha256").update(data).digest("base64url");
}

export function sanitizePath(base) {
    const normalized = path.normalize(path.join(process.env.STORAGE_LOCATION, base));
    const relative = path.relative(process.env.STORAGE_LOCATION, normalized);
    if (relative.includes("..")) throw new Error("Path insane");

    const parent = path.dirname(normalized);
    mkdirSync(parent, { recursive: true });
    
    return normalized;
}

export function getStoragePath(idp, sub) {
    const first2 = sub.substring(0, 2);
    const rest = sub.substring(2);

    const path = `${sha256sum(idp)}/${encodeURIComponent(first2)}/${encodeURIComponent(rest)}`;
    return sanitizePath(path);
}

export async function initializeUserTodos(idp, sub) {
    const client = createClient({
        url: `file://${getStoragePath(idp, sub)}`
    });

    await client.execute("CREATE TABLE IF NOT EXISTS todos(text TEXT NOT NULL, done BOOLEAN)");
    await client.close();
}

export async function getUserTodos(idp, sub) {
    const client = createClient({
        url: `file://${getStoragePath(idp, sub)}`
    });

    const rows = (await client.execute("SELECT *, rowid FROM todos")).rows;
    await client.close();
    return rows;
}

export async function addUserTodo(idp, sub, text) {
    const client = createClient({
        url: `file://${getStoragePath(idp, sub)}`
    });

    await client.execute("INSERT INTO todos(text, done) VALUES (?, ?)", [text, false]);
    await client.close();
}

export async function markUserTodoAsDone(idp, sub, rowid) {
    const client = createClient({
        url: `file://${getStoragePath(idp, sub)}`
    });

    await client.execute("UPDATE todos SET done = ? WHERE rowid = ?", [true, rowid]);
    await client.close();
}

export async function deleteUserTodo(idp, sub, rowid) {
    const client = createClient({
        url: `file://${getStoragePath(idp, sub)}`
    });

    await client.execute("DELETE FROM todos WHERE rowid = ?", [rowid]);
    await client.close();
}