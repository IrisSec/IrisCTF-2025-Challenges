import json
import struct
from pwn import *

NUM_PARTS = 100

# 0x10 : le or jle
# 4,9,15
# 12 add?
# 4,9 mem

OP_IDS = {
    10: "JMP",
    # 0x22: "LT",
    12: "ADD",
    5: "SUB",
    # 0x22: "JLE",
    19: "PUTCHAR",
    1: "GETCHAR",
    15: "LOAD",
    # 0x22: "JLT",
    3: "JNE",
    # 0x22: "GE",
    11: "EXIT",
    7: "JEQ",
    9: "MOV",
    # 0x22: "JGE",
    # 0x22: "GT",
    # 0x22: "JGT",
    # 0x22: "EQ",
    4: "STORE",
    17: "NE",
    0x22: "LE",

    # 4: "NOP",
    # 9: "NOP",

    # solve tools
    0xff: "JTENTRY",
    0x101: "PUSH",
    0x102: "POP",
    0x99: "NOP"
}
OP_IDS_JSON = json.dumps(OP_IDS)

NOP = 0x99
PUSH = 0x101
POP = 0x102

NOP_TARGETS = [0xa0,0xb00,0xb40]
# 0x541*4 stores regs

MEM_OFS = 0
INST_OFS = 2*1<<28
JT_OFS = 3*1<<28
ENTRY_OFS = 4*1<<28

DATA_SZ_B = 0x5a
INSTS_SZ = 0xb6
JT_SZ = 7

data_ptr = 0x550 * 4
inst_ptr_b = 0x5aa * 4
jt_ptr = 0x547 * 4 #TODO

first_locs = {}
sol_str = ""

FIRST_CHECK_INST = 0x2c0
N_CHECKS = 16
DIST = 8

for i in range(NUM_PARTS):
    print(i)
    DATA_SZ = DATA_SZ_B + len(str(i))
    inst_ptr = inst_ptr_b + 4 * len(str(i))

    with open(f"bins/{i}.bin", "rb") as f:
        f.read(8)
        ops_sz = struct.unpack("<I", f.read(4))[0]
        f.read(ops_sz)

        inst_sz = struct.unpack("<I", f.read(4))[0]
        f.read(inst_sz)

        data_sz = struct.unpack("<I", f.read(4))[0]
        data = f.read(data_sz)

        jt_sz = struct.unpack("<I", f.read(4))[0]
        f.read(jt_sz)

        print(ops_sz, inst_sz, data_sz, jt_sz, data[:32], data[inst_ptr:inst_ptr+32])

    if i == 0:
        seen = set()
        for j in range(0, INSTS_SZ):
            s_inst_ptr = inst_ptr + j * 16
            inst_data = [u32(data[s_inst_ptr+x:s_inst_ptr+x+4]) for x in range(0, 16, 4)]

            if inst_data[0] not in seen:
                print(s_inst_ptr, inst_data[0])
                first_locs[OP_IDS[inst_data[0]]] = j

            seen.add(inst_data[0])
        op_tbl = OP_IDS
    else:
        op_tbl = {}
        for v, ptr in first_locs.items():
            op_tbl[data[ptr * 16 + inst_ptr]] = v
        print(op_tbl)

    part = [""]*N_CHECKS
    for check in range(N_CHECKS):
        inst = check * 16 * DIST + FIRST_CHECK_INST + inst_ptr
        inst_data = [u32(data[inst+x:inst+x+4]) for x in range(0, 16, 4)]
        assert op_tbl[inst_data[0]] == "LOAD"
        idx = inst_data[2]
        inst = check * 16 * DIST + FIRST_CHECK_INST + inst_ptr + 16 * 6
        inst_data = [u32(data[inst+x:inst+x+4]) for x in range(0, 16, 4)]
        target_val = inst_data[2]

        for ci in range(5):
            inst = check * 16 * DIST + FIRST_CHECK_INST + inst_ptr + 16 * (ci + 1)
            inst_data = [u32(data[inst+x:inst+x+4]) for x in range(0, 16, 4)]
            if op_tbl[inst_data[0]] == "ADD":
                target_val -= inst_data[2]
            else:
                target_val += inst_data[2]

        part[idx] = chr(target_val & 0xffffff)

    sol_str += "".join(part)

print(sol_str)