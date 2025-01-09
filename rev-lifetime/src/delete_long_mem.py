import sys
with open(sys.argv[1]) as f:
    with open(sys.argv[2], "w") as ff:
        ismem = False
        for line in f:
            if ismem:
                if not line.startswith("	.long"):
                    ismem = False
                else:
                    continue
            if line.strip() == "mem:":
                ismem = True
            ff.write(line)