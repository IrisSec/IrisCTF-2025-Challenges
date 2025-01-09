#!/bin/python3 -u
import sys
import os

l = int(input("How many bytes? "))
print("Reading input.")

with open("/tmp/challenge-bin", "wb") as f:
    b = b""
    while len(b) < l:
        b += sys.stdin.buffer.read(l-len(b))
    f.write(b)

os.execv("/bin/sh", ["sh", "-c", "chmod +x /tmp/challenge-bin && /gem5.opt -d /tmp/out /challenge/challenge.py"])
