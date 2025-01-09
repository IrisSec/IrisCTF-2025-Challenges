import sys

inp = []
with open(sys.argv[1]) as f:
    for line in f:
        inp.append(line.strip().split(" "))

print(inp)
