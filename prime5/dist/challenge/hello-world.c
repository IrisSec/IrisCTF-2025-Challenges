#include <stdint.h>
#include <stddef.h>

const char* hello = "Hello world!\n";

void write(char* s, uint64_t len) {
    asm volatile("mov rsi, %[s];mov rdx, %[len];mov rdi, 1;mov rax, 1;syscall;" : : [s]"r"(s), [len]"r"(len) : "rax", "rsi", "rdi", "rdx");
}

void _start() {
    write(hello, 13);

    // Interact with challenge IO
    uint8_t data = 'w';
    asm volatile("out 77, al;" : : "a"(data));
    asm volatile("in al, 77;" : "=a"(data));

    // Exit
    asm volatile("mov rax, 60;syscall;");
}
