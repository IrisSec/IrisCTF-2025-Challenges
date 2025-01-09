#include <stdio.h>

const char* str = "hello world\n";

int main() {
    for(int i = 0; i < 12; i++) {
        putchar(str[i]);
    }
}