#include "chip8.h"
#include "test.h"

int main(int argv, char** argc) {
    Chip8VM_t* vm = malloc(sizeof(Chip8VM_t));
    initVM(vm, 100);
    if (loadROM(vm, "./chipgr8/data/roms/Tron.ch8")) {
        assert(fetch(vm) == 0x00E0);
        assert(fetch(vm) == 0xA34C);
        assert(fetch(vm) == 0x6312);
        assert(fetch(vm) == 0x640B);
        assert(fetch(vm) == 0xD349);
        assert(fetch(vm) == 0x7308);
        assert(fetch(vm) == 0xA355);
        assert(fetch(vm) == 0xD349);
        assert(fetch(vm) == 0x7308);
        assert(fetch(vm) == 0xA35E);
        assert(fetch(vm) == 0xD349);
        assert(fetch(vm) == 0x7308);
        assert(fetch(vm) == 0xA367);
        assert(fetch(vm) == 0xD349);
        assert(fetch(vm) == 0x6300);
        assert(fetch(vm) == 0x6400);
    } else {
        debugs("Failed to load rom.\n");
    }
    return 0;
}
