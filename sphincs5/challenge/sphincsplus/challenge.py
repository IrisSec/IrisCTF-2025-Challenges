import os
import sys
import secrets

print("Welcome to my super stable SPHINCS+ signing service.")
print("""===============
1. Get a signature
2. Try for the flag""")
os.system("./chal_genkey")

for attempt in range(256):
    choice = input("> ")

    if choice == "1":
        m = secrets.token_bytes(16)
        with open("/tmp/sphincs_req", "wb") as f:
            f.write(m)
        os.system("./chal_sign")
    elif choice == "2":
        smlen = int(input("Hex length: "))
        print("Hex-encoded signature: ", end="")
        rlen = 0
        m = ""
        while rlen < smlen:
            # ignore line breaks while reading because of
            # potential tty buffering
            m += sys.stdin.read(min(4096, smlen - rlen)).replace("\n","")
            rlen = len(m)

        m = bytes.fromhex(m)
        sys.stdin.readline()

        with open("/tmp/sphincs_ver", "wb") as f:
            f.write(m)
        os.system("./chal_verify")
    else:
        print("bye")
        exit()
