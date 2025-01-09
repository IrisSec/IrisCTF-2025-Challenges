import sys
import random

if len(sys.argv) < 3:
    print(f"usage: {sys.argv[0]} input.ctf output.c")
    exit(-1)

# types lsb - src is reg
# bit 1 - jmp is reg
# rest of bits - jmp
HEAD = """
#include <stdio.h>
//int getchar();
//int putchar(int x);

struct inst {{
    int opcode;
    int types;
    int src;
    int dst;
}};

int mem[1024] = {{0}};
int reg[6]; // A, B, C, D, BP, SP (not sure if we care to distinguish)
int pcs[{}] = {{ {} }};
int pc = 0;

"""

## Generate random op nums
OPS = ["MOV", "ADD", "SUB", "LD", "STR", "PUT", "GET", "EXIT", "CMPEQ", "CMPNE", "CMPLT", "CMPGT", "CMPLE", "CMPGE", "JEQ", "JNE", "JLT", "JGT", "JLE", "JGE", "JMP"]
OP_IDS = list(range(len(OPS)))
random.shuffle(OP_IDS)
OP_IDS = {k:v for k,v in zip(OPS, OP_IDS)}

## Emit code for ops
OP_CODES = {}
OP_CODES["MOV"] = """if(o->types & 1) {
    reg[o->dst] = reg[o->src];
} else {
    reg[o->dst] = o->src;
}
"""

OP_CODES["ADD"] = """if(o->types & 1) {
    reg[o->dst] += reg[o->src];
} else {
    reg[o->dst] += o->src;
}
reg[o->dst] &= 0xffffff;
"""

OP_CODES["SUB"] = """if(o->types & 1) {
    reg[o->dst] -= reg[o->src];
} else {
    reg[o->dst] -= o->src;
}
reg[o->dst] &= 0xffffff;
"""

OP_CODES["LD"] = """if(o->types & 1) {
    reg[o->dst] = mem[reg[o->src]];
} else {
    reg[o->dst] = mem[o->src];
}
"""

OP_CODES["STR"] = """if(o->types & 1) {
    mem[reg[o->src]] = reg[o->dst];
} else {
    mem[o->src] = reg[o->dst];
}
"""

OP_CODES["PUT"] = """if(o->types & 1) {
    putchar(reg[o->src] & 0xff);
} else {
    putchar(o->src & 0xff);
}
"""

OP_CODES["GET"] = """int tmp = getchar();
if(tmp != EOF) reg[o->dst] = tmp;
else reg[o->dst] = 0;
"""

OP_CODES["EXIT"] = """return 0;
"""

def gen_cmp(op):
    # FIXME ordering of comparison
    return f"""if(o->types & 1) {{
    reg[o->dst] = reg[o->dst] {op} reg[o->src];
}} else {{
    reg[o->dst] = reg[o->dst] {op} o->src;
}}
"""

OP_CODES["CMPEQ"] = gen_cmp("==")
OP_CODES["CMPNE"] = gen_cmp("!=")
OP_CODES["CMPLT"] = gen_cmp("<")
OP_CODES["CMPGT"] = gen_cmp(">")
OP_CODES["CMPGE"] = gen_cmp(">=")
OP_CODES["CMPLE"] = gen_cmp("<=")

def gen_jmp(op):
    return f"""if(o->types & 2) {{ // src is reg
    if(!(reg[o->dst] {op} reg[o->src])) {{}} // pass if cond fails
    else if(o->types & 1) pc = pcs[reg[o->types>>2]];
    else pc = pcs[o->types>>2];
}} else {{
    if(!(reg[o->dst] {op} o->src)) {{}} // pass if cond fails
    else if(o->types & 1) pc = pcs[reg[o->types>>2]];
    else pc = pcs[o->types>>2];
}}
"""

OP_CODES["JMP"] = """if(o->types & 2) pc = pcs[reg[o->types>>2]]; else pc = pcs[o->types>>2];
"""
OP_CODES["JEQ"] = gen_jmp("==")
OP_CODES["JNE"] = gen_jmp("!=")
OP_CODES["JLT"] = gen_jmp("<")
OP_CODES["JGT"] = gen_jmp(">")
OP_CODES["JLE"] = gen_jmp("<=")
OP_CODES["JGE"] = gen_jmp(">=")

infile = open(sys.argv[1])
current_pc = 0
pc_table = {}
insts = []
code = []
data = []
for line in infile:
    line = line.strip()
    if line.startswith(";") or len(line) == 0: continue
    if line.startswith("#"):
        pc_table[int(line[1:])] = current_pc
        continue

    # decode instruction
    inst = line.split(" ")

    if inst[0] == "data":
        data = inst[1:]
        continue

    if inst[0] not in OP_CODES:
        raise ValueError(f"unknown inst {inst[0]}")
    
    parsed = [inst[0], 0, 0, 0]

    if len(inst) > 1:
        if inst[1].isnumeric(): # dst (always reg)
            parsed[3] = int(inst[1])
        else:
            # only happens in jmp
            if inst[1] == "R": parsed[1] |= 2
            parsed[1] |= int(inst[2]) << 2

    if len(inst) > 3: # has src
        if inst[2] == "R":
            parsed[1] |= 1
            parsed[2] = int(inst[3])
        else:
            assert inst[2] == "I"
            parsed[2] = int(inst[3])

    if len(inst) > 5: # has jmp
        if inst[4] == "R":
            parsed[1] |= 2
            parsed[1] |= int(inst[5]) << 2
        else:
            assert inst[4] == "I"
            parsed[1] |= int(inst[5]) << 2

    code.append(parsed)

    current_pc += 1

infile.close()

# print(pc_table, max(pc_table), len(pc_table))
assert max(pc_table) == len(pc_table) - 1
# if max(pc_table) != len(pc_table) - 1:
#     for i in range(max(pc_table)):
#         if i not in pc_table:
#             pc_table[i] = len(code)

OP_TBL = list(OP_CODES.keys())
random.shuffle(OP_TBL)
OP_TBL = {OP_TBL[i]:i for i in range(len(OP_TBL))}

out = open(sys.argv[2], "w")

out.write(HEAD.format(len(pc_table), ",".join(str(pc_table[i]) for i in range(len(pc_table)))))
## write memory
last_nonzero = 0
for i in range(len(data)):
    if data[i] != "0":
        last_nonzero = i
# print("lnz", last_nonzero)
data = data[:last_nonzero+1]
out.write(f"const int rodata[{len(data)}] = {{ {",".join(data)} }};\n")
## write inst list
out.write(f"struct inst insts[{len(code)}] = {{")
codes = []
for inst in code:
    codes.append(f"{{.opcode = {OP_TBL[inst[0]]}, .types = {inst[1]}, .src = {inst[2]}, .dst = {inst[3]}}}")
out.write(",".join(codes))
out.write("};\n")
out.write(f"const int max_pc = {len(code)};\n")

out.write(f"""int main() {{
          for(int i = 0; i < {len(data)}; i++) mem[i] = rodata[i];""")
out.write("""
        while(pc < max_pc) {
        struct inst* o = &insts[pc];
        //printf("@ %d %d: %d %d %d\\n", pc, o->opcode, o->types, o->src, o->dst);
        //printf("regs: %d %d %d %d %d %d\\n", reg[0], reg[1], reg[2], reg[3], reg[4], reg[5]);
        pc++;
        switch(o->opcode) {
""")
## dump opcode impls
op_rand_order = list(OP_CODES.keys())
random.shuffle(op_rand_order)
for op in op_rand_order:
    out.write(f"            case ({OP_TBL[op]}): {{")
    out.write(OP_CODES[op])
    out.write("             break;}\n")
out.write("""
          }
    }
    return 0;
}
""")
out.close()