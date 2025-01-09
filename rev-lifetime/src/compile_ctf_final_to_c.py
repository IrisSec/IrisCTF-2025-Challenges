import sys
import random

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} output.c")
    exit(-1)

# types lsb - src is reg
# bit 1 - jmp is reg
# rest of bits - jmp
HEAD = """
#include <openssl/sha.h>
#include <stdio.h>

struct inst {
    int opcode;
    int types;
    int src;
    int dst;
};

// extra space
int mem[1<<25] = {0};
int reg[6]; // A, B, C, D, BP, SP (not sure if we care to distinguish)
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
input_buffer[input_ptr] = (char)tmp;
input_ptr++;
"""

OP_CODES["EXIT"] = """pc = max_pc;
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

pc_table_all = []
progs = []
data_all = []

for inf in range(100):
    inf = f"chal_parts/{inf}_ctf.ctf"
    infile = open(inf)
    current_pc = 0
    pc_table = {}
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

    assert max(pc_table) == len(pc_table) - 1
    data_all.append(data)
    progs.append(code)
    pc_table_all.append(pc_table)

OP_TBL = list(OP_CODES.keys())
random.shuffle(OP_TBL)
OP_TBL = {OP_TBL[i]:i for i in range(len(OP_TBL))}

out = open(sys.argv[1], "w")
out.write(HEAD)
for i, pc_table in enumerate(pc_table_all):
    out.write(f"int pcs{i}[] = {{" + ",".join(str(pc_table[i]) for i in range(len(pc_table))) + "};\n")
out.write("int* pcs_all[] = {" + ",".join(f"pcs{i}" for i in range(len(progs))) + "};\n")
## write memory
for i, data in enumerate(data_all):
    out.write(f"int rodata{i}[] = {{" + ",".join(data) + "};\n")
out.write(f"const int* rodata_all[] = {{ {",".join(f"rodata{i}" for i in range(len(progs)))} }};\n")
## write inst list
for i, code in enumerate(progs):
    codes = []
    for inst in code:
        codes.append(f"{{.opcode = {OP_TBL[inst[0]]}, .types = {inst[1]}, .src = {inst[2]}, .dst = {inst[3]}}}")
    out.write(f"struct inst insts{i}[] = {{" + ",".join(codes) + "};\n")

out.write(f"struct inst* insts_all[] = {{ {",".join(f"insts{i}" for i in range(len(progs)))} }};\n")

# FIXME len(code) could be different for each prog
out.write(f"const int max_pc = {len(code)};\n")

# FIXME len(data) could be different for each prog
out.write(f"""char input_buffer[{len(progs) * 16}];
int main() {{
    int input_ptr = 0;
    for(int prog = 0; prog < {len(progs)}; prog++) {{
    pc = 0;
    struct inst* insts = insts_all[prog];
    const int* rodata = rodata_all[prog];
    int* pcs = pcs_all[prog];
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
    }
          
    unsigned char hash[SHA256_DIGEST_LENGTH];

    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, input_buffer, """ + str(len(progs) * 16) + """);
    SHA256_Final(hash, &sha256);
    printf("This might be your flag, then: irisctf{");
    for(int i = 0; i < SHA256_DIGEST_LENGTH; i++) printf("%hhx", hash[i]);
    printf("}\\n");
    
    return 0;
}
""")
out.close()