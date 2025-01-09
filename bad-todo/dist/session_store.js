import { createClient } from "@libsql/client";

const client = createClient({
    url: process.env.SESSION_DB
});

export async function initSessionStore() {
    await client.execute(`CREATE TABLE IF NOT EXISTS sessions(
        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(32)))),
        idpUrl TEXT NOT NULL,
        clientId TEXT NOT NULL,
        userId TEXT,
        userMetadata TEXT
    )`)
}

export async function newSession(idp, clientId) {
    const sessionId = (await client.execute("INSERT INTO sessions (idpUrl, clientId) VALUES(?, ?) RETURNING id", [idp, clientId])).rows[0].id;
    return sessionId;
}

export async function lookupSession(session) {
    const { rows } = await client.execute("SELECT * FROM sessions WHERE id = ?", [session]);
    if (rows.length !== 1) throw new Error("Invalid session");

    return rows[0];
}

export async function successfulLogin(session, metadata) {
    await client.execute("UPDATE sessions SET userId = ?, userMetadata = ? WHERE id = ?", [metadata.sub, JSON.stringify(metadata), session]);
}

export async function getUser(session) {
    const { rows } = await client.execute("SELECT * FROM sessions WHERE id = ?", [session]);
    if (rows.length !== 1) return false;

    if (!rows[0].userId) return false;

    return rows[0];
}