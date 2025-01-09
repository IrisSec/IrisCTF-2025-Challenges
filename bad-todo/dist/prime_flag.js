import { promises as fs, existsSync } from "fs";
import { createClient } from "@libsql/client";

export async function primeFlag() {
    if (existsSync(process.env.STORAGE_LOCATION + "/flag")) {
        await fs.chmod(process.env.STORAGE_LOCATION + "/flag", 0o700);
        await fs.rm(process.env.STORAGE_LOCATION + "/flag");
    }
    
    const client = createClient({
        url: `file://${process.env.STORAGE_LOCATION}/flag`
    });

    await client.execute("CREATE TABLE todos(text TEXT NOT NULL, done BOOLEAN)");
    await client.execute("INSERT INTO todos(text, done) VALUES(?, ?)", [process.env.FLAG, true]);
    await client.close();

    await fs.chmod(process.env.STORAGE_LOCATION + "/flag", 0o400);
}