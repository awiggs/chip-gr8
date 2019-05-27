#ifndef DEBUG
    #define DEBUG
#endif

#include <stdio.h>
#include "chip8.h"

int main(int argv, char** argc) {
    Chip8VM_t* vm = initVM();
    if (loadROM(vm, "./data/roms/Tron.ch8")) {
        for (int i = 0; i < 10; i++) {
            debugf("The %ith instruction is %02x.\n", i, fetch(vm));
        }
        unloadROM(vm);
    } else {
        debugs("Failed to load rom.\n");
    }
    return 0;
}
