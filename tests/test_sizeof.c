#include "chip8.h"

int main() {
    printf("sizeof(u8)  = %lu\n", sizeof(u8));
    printf("sizeof(u16) = %lu\n", sizeof(u16));
    printf("sizeof(u32) = %lu\n", sizeof(u32));
    printf("sizeof(u64) = %lu\n", sizeof(u64));
    printf("sizeof(s8)  = %lu\n", sizeof(s8));
    printf("sizeof(s16) = %lu\n", sizeof(s16));
    printf("sizeof(s32) = %lu\n", sizeof(s32));
    printf("sizeof(s64) = %lu\n", sizeof(s64));
    printf("sizeof(Chip8VM_T) = %lu\n", sizeof(Chip8VM_t));
    return 0;
}
