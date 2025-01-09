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

for i in range(NUM_PARTS):
    print(i)
    DATA_SZ = DATA_SZ_B + len(str(i))
    inst_ptr = inst_ptr_b + len(str(i)) * 4

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

   data = bytearray(data)
    for n in NOP_TARGETS:
        data[inst_ptr+n] = NOP

    with open(f"bins_nest/{i}.bin", "wb") as f:
        f.write(b"ICTFCHAL")
        f.write(p32(len(OP_IDS_JSON)))
        f.write(OP_IDS_JSON.encode())
        f.write(p32(INSTS_SZ*16+16))
        f.write(p32(0xff) + p32(0) + p32(0) + p32(0))
        f.write(data[inst_ptr:inst_ptr+INSTS_SZ*16])
        f.write(p32(DATA_SZ*4))
        f.write(data[data_ptr:data_ptr+DATA_SZ*4])
        f.write(p32(JT_SZ*4))
        for j in range(jt_ptr, jt_ptr+JT_SZ*4, 4):
            f.write(p32(u32(data[j:j+4]) * 16 + INST_OFS))
