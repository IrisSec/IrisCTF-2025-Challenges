#include <stdio.h>
#define __USE_GNU
#include <signal.h>
#include <stdlib.h>
#include <stdint.h>
#include <ucontext.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include "ops.h"
#define byte uint8_t
#define ushort uint16_t
#define uint uint32_t
#define ulong uint64_t

void* CODEMEM = NULL;
size_t CODESZ = 0;

void* GPMEM = NULL;
size_t GPMEMSZ = 0xffff;

byte makeModRmRr(byte r0, byte r1) {
    return 0xc0 | ((r0 & 7) << 3) | (r1 & 7);
}

void codeWrite() {
    if (mprotect(CODEMEM, CODESZ, PROT_WRITE | PROT_READ) == -1) {
        exit(1);
    }
}

void codeExecute() {
    if (mprotect(CODEMEM, CODESZ, PROT_EXEC | PROT_READ) == -1) {
        exit(1);
    }
}

void handler(int sig, siginfo_t *si, void *context) {
    ucontext_t *uc = (ucontext_t *)context;
    byte* pc = (byte*)uc->uc_mcontext.gregs[REG_RIP];
    byte pcOpc = *pc;

    codeWrite();

    switch (pcOpc) {
        case OPC_ADD: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x01;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x90909090;
            *((ushort*)(&pc[6])) = 0x9090;
            break;
        }
        case OPC_SUB: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x29;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x90909090;
            *((ushort*)(&pc[6])) = 0x9090;
            break;
        }
        case OPC_CLR: {
            byte r0 = pc[1];
            pc[0] = 0x31;
            pc[1] = makeModRmRr(r0, r0);
            *((uint*)(&pc[2])) = 0x90909090;
            *((ushort*)(&pc[6])) = 0x9090;
            break;
        }
        case OPC_MOV: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x89;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x90909090;
            *((ushort*)(&pc[6])) = 0x9090;
            break;
        }
        case OPC_MOVC: {
            byte r0 = pc[1];
            uint v = *((uint*)(&pc[3]));
            pc[0] = 0xb8 | (r0 & 7);
            *((uint*)(&pc[1])) = v;
            pc[5] = 0x90;
            *((ushort*)(&pc[6])) = 0x9090;
            break;
        }
        case OPC_EQ: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x39;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x0fc0950f;
            *((ushort*)(&pc[6])) = 0xc0b6;
            break;
        }
        case OPC_NEQ: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x39;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x0fc0940f;
            *((ushort*)(&pc[6])) = 0xc0b6;
            break;
        }
        case OPC_LT: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x39;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x0fc09c0f;
            *((ushort*)(&pc[6])) = 0xc0b6;
            break;
        }
        case OPC_LTE: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x39;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x0fc09e0f;
            *((ushort*)(&pc[6])) = 0xc0b6;
            break;
        }
        case OPC_GT: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x39;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x0fc09f0f;
            *((ushort*)(&pc[6])) = 0xc0b6;
            break;
        }
        case OPC_GTE: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x39;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x0fc09d0f;
            *((ushort*)(&pc[6])) = 0xc0b6;
            break;
        }
        case OPC_AND: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x21;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x90909090;
            *((ushort*)(&pc[6])) = 0x9090;
            break;
        }
        case OPC_OR: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x09;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x90909090;
            *((ushort*)(&pc[6])) = 0x9090;
            break;
        }
        case OPC_XOR: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x31;
            pc[1] = makeModRmRr(r1, r0);
            *((uint*)(&pc[2])) = 0x90909090;
            *((ushort*)(&pc[6])) = 0x9090;
            break;
        }
        case OPC_JMP: {
            uint v = *((uint*)(&pc[3]));
            byte* offTar = ((byte*)CODEMEM) + v * 8;
            byte* offFrom = pc + 5;
            int offRel = offTar - offFrom;
            pc[0] = 0xe9;
            *((int*)(&pc[1])) = offRel;
            pc[5] = 0x90;
            *((ushort*)(&pc[6])) = 0x9090;
            break;
        }
        case OPC_JMPC: {
            byte r0 = pc[1];
            uint v = *((uint*)(&pc[3]));
            byte* offTar = ((byte*)CODEMEM) + v * 8;
            byte* offFrom = pc + 8;
            int offRel = offTar - offFrom;
            pc[0] = 0x85;
            pc[1] = makeModRmRr(r0, r0);
            *((ushort*)(&pc[2])) = 0x840f;
            *((int*)(&pc[4])) = offRel;
            break;
        }
        case OPC_RMEM: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x42;
            pc[1] = 0x8b;
            pc[2] = 0x04 | ((r0 & 7) << 3);
            pc[3] = r1 & 7;
            *((uint*)(&pc[4])) = 0x90909090;
            break;
        }
        case OPC_WMEM: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            pc[0] = 0x42;
            pc[1] = 0x89;
            pc[2] = 0x04 | ((r0 & 7) << 3);
            pc[3] = r1 & 7;
            *((uint*)(&pc[4])) = 0x90909090;
            break;
        }
        case OPC_CALL: {
            uint v = *((uint*)(&pc[3]));
            byte* offTar = ((byte*)CODEMEM) + v * 8;
            byte* offFrom = pc + 5;
            int offRel = offTar - offFrom;
            pc[0] = 0xe8;
            *((int*)(&pc[1])) = offRel;
            pc[5] = 0x90;
            *((ushort*)(&pc[6])) = 0x9090;
            break;
        }
        case OPC_RET: {
            //pc[0] = 0xc3;
            *((uint*)(&pc[0])) = 0x909090c3;
            *((uint*)(&pc[4])) = 0x90909090;
            break;
        }
        case OPC_MEMPTR: {
            byte r0 = pc[1];
            byte r1 = pc[2];
            *((ushort*)(&pc[0])) = 0x8d4a;
            pc[2] = 0x04 | ((r0 & 7) << 3);
            pc[3] = r1 & 7;
            *((uint*)(&pc[4])) = 0x90909090;
            break;
        }
        case OPC_SYSCALL: {
            //((ushort*)(&pc[0])) = 0x050f;
            *((uint*)(&pc[0])) = 0x9090050f;
            *((uint*)(&pc[4])) = 0x90909090;
            break;
        }
		default: {
			// xor rax, rax
			// return
			break;
		}
    }

    codeExecute();
}

int main() {
    struct sigaction sa;
    sa.sa_flags = SA_SIGINFO;
    sa.sa_sigaction = handler;
    sigaction(SIGILL, &sa, NULL);
    
    unsigned char code[] = (
        // 00: write flag
        "\x17" "\x00\x00" "\x00\x10\x00\x00\x00" // OPC_MOVC R0 0x00001000
        "\x17" "\x01\x00" "\x66\x6C\x61\x67\x00" // OPC_MOVC R1 0x67616C66
        "\xc5" "\x01\x00" "\x00\x00\x00\x00\x00" // OPC_WMEM R1 *R0

        // 03: write ? \x00\x00
        "\x17" "\x00\x00" "\x04\x10\x00\x00\x00" // OPC_MOVC R0 0x00001004
        "\x17" "\x01\x00" "\x3F\x20\x00\x00\x00" // OPC_MOVC R1 0x0000203F
        "\xc5" "\x01\x00" "\x00\x00\x00\x00\x00" // OPC_WMEM R1 *R0

        // 06: print above string
        "\x17" "\x01\x00" "\x00\x10\x00\x00\x00" // OPC_MOVC R1 0x00001000 (RSI offset)
        "\x17" "\x00\x00" "\x01\x00\x00\x00\x00" // OPC_MOVC R0 0x00000001 (RAX)
        "\x17" "\x07\x00" "\x01\x00\x00\x00\x00" // OPC_MOVC R7 0x00000001 (RDI)
        "\xd6" "\x06\x01" "\x00\x00\x00\x00\x00" // OPC_MEMPTR R6 (RSI)
        "\x17" "\x02\x00" "\x06\x00\x00\x00\x00" // OPC_MOVC R2 0x00000006 (RDX)
        "\xea" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_SYSCALL

        // 0c: read input to 0x2000
        "\x17" "\x01\x00" "\x00\x20\x00\x00\x00" // OPC_MOVC R1 0x00002000 (RSI offset)
        "\x0e" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_CLR R0 (RAX)
        "\x0e" "\x07\x00" "\x00\x00\x00\x00\x00" // OPC_CLR R7 (RDI)
        "\xd6" "\x06\x01" "\x00\x00\x00\x00\x00" // OPC_MEMPTR R6 (RSI)
        "\x17" "\x02\x00" "\x20\x00\x00\x00\x00" // OPC_MOVC R2 0x00000020 (RDX)
        "\xea" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_SYSCALL

        // 12: loop 1 setup
        "\x17" "\x02\x00" "\x00\x00\x00\x00\x00" // OPC_MOVC R2 0x00000000 (checksum value)
        "\x17" "\x03\x00" "\x1f\x00\x00\x00\x00" // OPC_MOVC R3 0x0000001F
        // 14: loop 1 top
        "\x17" "\x00\x00" "\x00\x20\x00\x00\x00" // OPC_MOVC R0 0x00002000 (read offset)
        "\x06" "\x00\x03" "\x00\x00\x00\x00\x00" // OPC_ADD R0 R3
        "\xc4" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_RMEM R0 *R0
        "\x17" "\x01\x00" "\xff\x00\x00\x00\x00" // OPC_MOVC R1 0x000000FF
        "\x60" "\x00\x01" "\xff\x00\x00\x00\x00" // OPC_AND R0 R1
        "\x06" "\x02\x00" "\x00\x00\x00\x00\x00" // OPC_ADD R2 R0

        "\x17" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_MOVC R0 0x00000000
        "\x1e" "\x03\x00" "\x00\x00\x00\x00\x00" // OPC_EQ R3 R0
        "\x9a" "\x00\x00" "\x20\x00\x00\x00\x00" // OPC_JMPC R0 0x00000020

        "\x17" "\x00\x00" "\x01\x00\x00\x00\x00" // OPC_MOVC R0 0x00000001
        "\x07" "\x03\x00" "\x00\x00\x00\x00\x00" // OPC_SUB R3 R0
        "\x82" "\x00\x00" "\x14\x00\x00\x00\x00" // OPC_JMP 0x00000014

        // ///////////////

        // 20: return 1 if not 0xcff checksum
        "\x17" "\x00\x00" "\xff\x0c\x00\x00\x00" // OPC_MOVC R0 0x00000CFF
        "\x1e" "\x00\x02" "\x00\x00\x00\x00\x00" // OPC_EQ R0 R2
        "\x9a" "\x00\x00" "\x25\x00\x00\x00\x00" // OPC_JMPC R0 0x00000025
        "\x17" "\x00\x00" "\x01\x00\x00\x00\x00" // OPC_MOVC R0 0x00000001
        "\xd5" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_RET

        // 25: xor check 1
        "\x17" "\x01\x00" "\x00\x20\x00\x00\x00" // OPC_MOVC R1 0x00002000 (offset)
        "\xc4" "\x00\x01" "\x00\x00\x00\x00\x00" // OPC_RMEM R0 *R1
        "\x17" "\x02\x00" "\xd7\xb0\x51\xbf\x00" // OPC_MOVC R2 0xbf51b0d7 (xor value)
        "\x62" "\x02\x00" "\x00\x00\x00\x00\x00" // OPC_XOR R2 R0

        "\x17" "\x00\x00" "\xbe\xc2\x38\xcc\x00" // OPC_MOVC R0 0xCC38C2BE
        "\x1e" "\x00\x02" "\x00\x00\x00\x00\x00" // OPC_EQ R0 R2
        "\x9a" "\x00\x00" "\x2e\x00\x00\x00\x00" // OPC_JMPC R0 0x0000002E
        "\x17" "\x00\x00" "\x02\x00\x00\x00\x00" // OPC_MOVC R0 0x00000002
        "\xd5" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_RET

        // 2e: xor check 2
        "\x17" "\x01\x00" "\x04\x20\x00\x00\x00" // OPC_MOVC R1 0x00002004 (offset)
        "\xc4" "\x00\x01" "\x00\x00\x00\x00\x00" // OPC_RMEM R0 *R1
        "\x17" "\x02\x00" "\x7b\x54\xcc\x75\x00" // OPC_MOVC R2 0x75cc547b (xor value)
        "\x62" "\x02\x00" "\x00\x00\x00\x00\x00" // OPC_XOR R2 R0

        "\x17" "\x00\x00" "\x18\x20\xaa\x0e\x00" // OPC_MOVC R0 0x0EAA2018
        "\x1e" "\x00\x02" "\x00\x00\x00\x00\x00" // OPC_EQ R0 R2
        "\x9a" "\x00\x00" "\x37\x00\x00\x00\x00" // OPC_JMPC R0 0x00000037
        "\x17" "\x00\x00" "\x03\x00\x00\x00\x00" // OPC_MOVC R0 0x00000003
        "\xd5" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_RET

        // 37: xor check 3
        "\x17" "\x01\x00" "\x08\x20\x00\x00\x00" // OPC_MOVC R1 0x00002008 (offset)
        "\xc4" "\x00\x01" "\x00\x00\x00\x00\x00" // OPC_RMEM R0 *R1
        "\x17" "\x02\x00" "\x3a\xd8\x0f\x4f\x00" // OPC_MOVC R2 0x4f0fd83a (xor value)
        "\x62" "\x02\x00" "\x00\x00\x00\x00\x00" // OPC_XOR R2 R0

        "\x17" "\x00\x00" "\x4d\xb7\x78\x10\x00" // OPC_MOVC R0 0x1078B74D
        "\x1e" "\x00\x02" "\x00\x00\x00\x00\x00" // OPC_EQ R0 R2
        "\x9a" "\x00\x00" "\x40\x00\x00\x00\x00" // OPC_JMPC R0 0x00000040
        "\x17" "\x00\x00" "\x04\x00\x00\x00\x00" // OPC_MOVC R0 0x00000004
        "\xd5" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_RET

        // 40: xor check 4
        "\x17" "\x01\x00" "\x0c\x20\x00\x00\x00" // OPC_MOVC R1 0x0000200c (offset)
        "\xc4" "\x00\x01" "\x00\x00\x00\x00\x00" // OPC_RMEM R0 *R1
        "\x17" "\x02\x00" "\x44\x77\x11\xa2\x00" // OPC_MOVC R2 0xa2117744 (xor value)
        "\x62" "\x02\x00" "\x00\x00\x00\x00\x00" // OPC_XOR R2 R0

        "\x17" "\x00\x00" "\x32\x12\x63\xdb\x00" // OPC_MOVC R0 0xDB631232
        "\x1e" "\x00\x02" "\x00\x00\x00\x00\x00" // OPC_EQ R0 R2
        "\x9a" "\x00\x00" "\x49\x00\x00\x00\x00" // OPC_JMPC R0 0x00000049
        "\x17" "\x00\x00" "\x05\x00\x00\x00\x00" // OPC_MOVC R0 0x00000005
        "\xd5" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_RET

        // ///////////////

        // 49: xor check 5
        "\x17" "\x01\x00" "\x10\x20\x00\x00\x00" // OPC_MOVC R1 0x00002010 (offset)
        "\xc4" "\x00\x01" "\x00\x00\x00\x00\x00" // OPC_RMEM R0 *R1
        "\x17" "\x02\x00" "\xc6\xce\xd0\xec\x00" // OPC_MOVC R2 0xecd0cec6 (xor value)
        "\x62" "\x02\x00" "\x00\x00\x00\x00\x00" // OPC_XOR R2 R0

        "\x17" "\x00\x00" "\x99\xa1\xa0\x98\x00" // OPC_MOVC R0 0x98A0A199
        "\x1e" "\x00\x02" "\x00\x00\x00\x00\x00" // OPC_EQ R0 R2
        "\x9a" "\x00\x00" "\x52\x00\x00\x00\x00" // OPC_JMPC R0 0x00000052
        "\x17" "\x00\x00" "\x06\x00\x00\x00\x00" // OPC_MOVC R0 0x00000006
        "\xd5" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_RET

        // 52: xor check 6
        "\x17" "\x01\x00" "\x14\x20\x00\x00\x00" // OPC_MOVC R1 0x00002014 (offset)
        "\xc4" "\x00\x01" "\x00\x00\x00\x00\x00" // OPC_RMEM R0 *R1
        "\x17" "\x02\x00" "\xfa\xf9\x19\x2e\x00" // OPC_MOVC R2 0x2e19f9fa (xor value)
        "\x62" "\x02\x00" "\x00\x00\x00\x00\x00" // OPC_XOR R2 R0

        "\x17" "\x00\x00" "\x93\x94\x78\x42\x00" // OPC_MOVC R0 0x42789493
        "\x1e" "\x00\x02" "\x00\x00\x00\x00\x00" // OPC_EQ R0 R2
        "\x9a" "\x00\x00" "\x5b\x00\x00\x00\x00" // OPC_JMPC R0 0x0000005B
        "\x17" "\x00\x00" "\x07\x00\x00\x00\x00" // OPC_MOVC R0 0x00000007
        "\xd5" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_RET

        // 5b: xor check 7
        "\x17" "\x01\x00" "\x18\x20\x00\x00\x00" // OPC_MOVC R1 0x00002018 (offset)
        "\xc4" "\x00\x01" "\x00\x00\x00\x00\x00" // OPC_RMEM R0 *R1
        "\x17" "\x02\x00" "\xd9\x83\xea\x32\x00" // OPC_MOVC R2 0x32ea83d9 (xor value)
        "\x62" "\x02\x00" "\x00\x00\x00\x00\x00" // OPC_XOR R2 R0

        "\x17" "\x00\x00" "\x86\xe0\x85\x56\x00" // OPC_MOVC R0 0x5685E086
        "\x1e" "\x00\x02" "\x00\x00\x00\x00\x00" // OPC_EQ R0 R2
        "\x9a" "\x00\x00" "\x64\x00\x00\x00\x00" // OPC_JMPC R0 0x00000064
        "\x17" "\x00\x00" "\x08\x00\x00\x00\x00" // OPC_MOVC R0 0x00000008
        "\xd5" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_RET

        // 64: xor check 8
        "\x17" "\x01\x00" "\x1c\x20\x00\x00\x00" // OPC_MOVC R1 0x0000201c (offset)
        "\xc4" "\x00\x01" "\x00\x00\x00\x00\x00" // OPC_RMEM R0 *R1
        "\x17" "\x02\x00" "\xe0\x61\xeb\xe5\x00" // OPC_MOVC R2 0xe5eb61e0 (xor value)
        "\x62" "\x02\x00" "\x00\x00\x00\x00\x00" // OPC_XOR R2 R0

        "\x17" "\x00\x00" "\x85\x40\xca\x98\x00" // OPC_MOVC R0 0x98CA4085
        "\x1e" "\x00\x02" "\x00\x00\x00\x00\x00" // OPC_EQ R0 R2
        "\x9a" "\x00\x00" "\x6d\x00\x00\x00\x00" // OPC_JMPC R0 0x0000006D
        "\x17" "\x00\x00" "\x09\x00\x00\x00\x00" // OPC_MOVC R0 0x00000009
        "\xd5" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_RET

        // 6d: exit
        "\x17" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_MOVC R0 0
        "\xd5" "\x00\x00" "\x00\x00\x00\x00\x00" // OPC_RET
    );
    CODESZ = sizeof(code);
    
    CODEMEM = mmap(NULL, CODESZ, PROT_WRITE | PROT_READ, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (CODEMEM == MAP_FAILED) {
        return 1;
    }
    
    GPMEM = mmap(NULL, GPMEMSZ, PROT_WRITE | PROT_READ, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (GPMEM == MAP_FAILED) {
        return 1;
    }

    memcpy(CODEMEM, code, CODESZ);

    if (mprotect(CODEMEM, CODESZ, PROT_EXEC | PROT_READ) == -1) {
        return 1;
    }
    if (mprotect(GPMEM, GPMEMSZ, PROT_WRITE | PROT_READ) == -1) {
        return 1;
    }
    asm volatile ("mov %0, %%r8" : : "r" ((ulong)GPMEM));
    asm volatile ("xor %rax, %rax");
    asm volatile ("xor %rcx, %rcx");
    asm volatile ("xor %rdx, %rdx");
    asm volatile ("xor %rbx, %rbx");
    asm volatile ("xor %rsi, %rsi");
    asm volatile ("xor %rdi, %rdi");

    int (*func)() = CODEMEM;
    int result = func();

    if (result == 0) {
        printf("Program returned \"correct\"!\n");
    } else {
        printf("Program returned \"incorrect\" (%d).\n", result);
    }

    munmap(CODEMEM, CODESZ);
    munmap(GPMEM, GPMEMSZ);
    return result;
}