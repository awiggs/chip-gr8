#include "chip8.h"
#include "test.h"

int main() {
    Chip8VM_t* vm = malloc(sizeof(Chip8VM_t));
    initVM(vm, 100);

    // Hexsprite 0
    assert(vm->hexes[0] == 0xF0);
    assert(vm->hexes[1] == 0x90);
    assert(vm->hexes[2] == 0x90);
    assert(vm->hexes[3] == 0x90);
    assert(vm->hexes[4] == 0xF0);

    // Hexsprite 7
    assert(vm->hexes[7 * 5 + 0] == 0xF0);
    assert(vm->hexes[7 * 5 + 1] == 0x10);
    assert(vm->hexes[7 * 5 + 2] == 0x20);
    assert(vm->hexes[7 * 5 + 3] == 0x40);
    assert(vm->hexes[7 * 5 + 4] == 0x40);

    // Hexsprite A
    assert(vm->hexes[10 * 5 + 0] == 0xF0);
    assert(vm->hexes[10 * 5 + 1] == 0x90);
    assert(vm->hexes[10 * 5 + 2] == 0xF0);
    assert(vm->hexes[10 * 5 + 3] == 0x90);
    assert(vm->hexes[10 * 5 + 4] == 0x90);

    // Hexsprite F
    assert(vm->hexes[15 * 5 + 0] == 0xF0);
    assert(vm->hexes[15 * 5 + 1] == 0x80);
    assert(vm->hexes[15 * 5 + 2] == 0xF0);
    assert(vm->hexes[15 * 5 + 3] == 0x80);
    assert(vm->hexes[15 * 5 + 4] == 0x80);

    return 0;
}
