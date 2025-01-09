#!/bin/python3
import sys
import os

l = int(input("How many bytes? "))
print("Reading input.")

with open("challenge-bin", "wb") as f:
    f.write(sys.stdin.buffer.read(l))

os.execv("/bin/sh", ["sh", "-c", "chmod +x challenge-bin && /gem5.opt /challenge/challenge.py"])
