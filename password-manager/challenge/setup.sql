CREATE DATABASE uwu;
use uwu;

CREATE TABLE IF NOT EXISTS passwords ( URL text, Title text, Username text, Password text ) DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE utf8mb4_0900_as_cs;
INSERT INTO passwords ( URL, Title, Username, Password ) VALUES ( "https://example.com", "Discord", "skat@skat.skat", "mypasswordisskat");
INSERT INTO passwords ( URL, Title, Username, Password ) VALUES ( "https://example.com", "RF-Quabber Forum", "skat", "irisctf{l00k5_l1k3_w3_h4v3_70_t34ch_sk47_h0w_70_r3m3mb3r_s7uff}");
INSERT INTO passwords ( URL, Title, Username, Password ) VALUES ( "https://2025.irisc.tf", "Iris CTF", "skat", "this-isnt-a-real-password");

CREATE USER 'readonly_user'@'%' IDENTIFIED BY 'password';
GRANT SELECT ON uwu.passwords TO 'readonly_user'@'%';
FLUSH PRIVILEGES;