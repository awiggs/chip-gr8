#include "chip8.h"

void miniDRW(u8 x, u8 y) {
    // calculate the intended coordinates
    u8 row = (y) % 32;
    u8 col = x;
    
    // calculate corresponding location in VRAM
    u16 bit         = ((row * 64) + col);
    u16 firstByte    = bit / 8;
    u16 secondByte   = x >= 56 ? (row * 8) : firstByte + 1;
    u8 bitOffset    = bit % 8;
    u8 leftoverBits = 8 - bitOffset;
    
    printf("(%d, %d) -> \n  bit:\t\t%d\n  firstByte:\t%d\n  secondByte:\t%d\n  bitOffset:\t%d\n  leftoverBits:\t%d\n",
        x, y,
        bit,
        firstByte,
        secondByte,
        bitOffset,
        leftoverBits
    );
}

int main() {
    miniDRW(60, 20);
    
    Chip8VM_t vm;
    initVM(&vm);
    
    printf("RAM[0]: %x\n", vm.hexes[10]);
    
    freeVM(&vm);
}
