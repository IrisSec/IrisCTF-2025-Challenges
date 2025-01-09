import sys
from pwn import *
from tqdm import tqdm
import json

NUM_PARTS = 100


OP_IDS = {
    0: "JMP",
    1: "LT",
    2: "ADD",
    3: "SUB",
    4: "JLE",
    5: "PUTCHAR",
    6: "GETCHAR",
    7: "LOAD",
    8: "JLT",
    9: "JNE",
    0xa: "GE",
    0xb: "EXIT",
    0xc: "JEQ",
    0xd: "MOV",
    0xe: "JGE",
    0xf: "GT",
    0x10: "JGT",
    0x11: "EQ",
    0x12: "STORE",
    0x13: "NE",
    0x14: "LE",
    0xff: "JTENTRY",
    0x101: "PUSH",
    0x102: "POP",
    0x100: "NOP"
}
OP_IDS_JSON = json.dumps(OP_IDS)

NOP = 0x100
PUSH = 0x101
POP = 0x102

MEM_OFS = 0
INST_OFS = 2*1<<28
JT_OFS = 3*1<<28
ENTRY_OFS = 4*1<<28

DATA_SZ_B = 0x885 # num of 32-bit words per data section
INSTS_SZ = 0x3a2e # num of 16-byte instructions

chal_file = ELF("./chal_v1")
insts_base = chal_file.vaddr_to_offset(0x17eb080)
data_base = chal_file.vaddr_to_offset(0x130de0)
jt_base = chal_file.vaddr_to_offset(0x5b640)

jt_0 = u64(chal_file.data[jt_base+0*8:jt_base+0*8+8])
jt_1 = u64(chal_file.data[jt_base+1*8:jt_base+1*8+8])
JT_SZ = (jt_1 - jt_0) // 4 # 32-bit words

insts_ptrs = []
for i in range(NUM_PARTS):
    print(i)
    DATA_SZ = DATA_SZ_B + len(str(i))
    inst_ptr = u64(chal_file.data[insts_base+i*8:insts_base+i*8+8])
    inst_ptr = chal_file.vaddr_to_offset(inst_ptr)
    jt_ptr = u64(chal_file.data[jt_base+i*8:jt_base+i*8+8])
    jt_ptr = chal_file.vaddr_to_offset(jt_ptr)
    data_ptr = u64(chal_file.data[data_base+i*8:data_base+i*8+8])
    data_ptr = chal_file.vaddr_to_offset(data_ptr)

    with open(f"bins/{i}.bin", "wb") as f:
        f.write(b"ICTFCHAL")

        f.write(p32(len(OP_IDS_JSON)))
        f.write(OP_IDS_JSON.encode())
        f.write(p32(INSTS_SZ*16+16))
        f.write(p32(0xff) + p32(0) + p32(0) + p32(0))
        f.write(chal_file.data[inst_ptr:inst_ptr+INSTS_SZ*16])
        f.write(p32(DATA_SZ*4))
        f.write(chal_file.data[data_ptr:data_ptr+DATA_SZ*4])
        f.write(p32(JT_SZ*4))
        for j in range(jt_ptr, jt_ptr+JT_SZ*4, 4):
            f.write(p32(u32(chal_file.data[j:j+4]) * 16 + INST_OFS))
