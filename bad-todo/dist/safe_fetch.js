import { promises as dns } from "dns";
import ipaddr from "ipaddr.js";

const unsafeIps = {forbidden:[
    [ ipaddr.parse("10.0.0.0"), 8 ],
    [ ipaddr.parse("172.16.0.0"), 12 ],
    [ ipaddr.parse("192.168.0.0"), 16 ],
    [ ipaddr.parse("100.64.0.0"), 10 ],
    [ ipaddr.parse("169.254.0.0"), 16 ],
    [ ipaddr.parse("127.0.0.0"), 8 ],
    [ ipaddr.parse("fd00::"), 7 ],
    [ ipaddr.parse("fe80::"), 10 ],
]}

async function cappedReader(stream, limit) {
    const buffer = new ArrayBuffer(limit);
    const bufferView = new Uint8Array(buffer);
    let pointer = 0;

    while (1) {
        const { value, done } = await stream.read();

        if (done) break;
        if (value.length + pointer > limit) {
            await stream.cancel();
            throw new Error("Stream too chunky");
        }
    
        bufferView.set(value, pointer);
        pointer += value.length;
    }

    return bufferView.slice(0, pointer);
}

export async function safeFetch(url, params) {
    const urlParsed = new URL(url);
    if (urlParsed.protocol !== "https:") throw new Error("use https");

    const resolved = await dns.resolve(urlParsed.host);
    const isOk = resolved.every(ip => {
        const parsed = ipaddr.parse(ip);
        const match = ipaddr.subnetMatch(parsed, unsafeIps, "ok");

        return match === "ok";
    });

    if (!isOk) throw new Error("unsafe url");
    
    return await fetch(url, params);
}

export async function safeJson(url, params) {
    const response = await safeFetch(url, params);

    if (response.status !== 200) return false;
    if (!response.body) return false;

    const reader = response.body.getReader();

    const data = await cappedReader(reader, 0xFFFF);
    const decoder = new TextDecoder();
    const str = decoder.decode(data);

    return JSON.parse(str);
}