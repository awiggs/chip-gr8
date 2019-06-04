#include "chip8.h"
#include "test.h"

void test_basic() {
    Chip8VM_t* vm = initVM();

    // LD V0 0x4
    vm->RAM[0x200] = 0x60;
    vm->RAM[0x201] = 0x04;
    // ADD V0 0x3
    vm->RAM[0x202] = 0x70;
    vm->RAM[0x203] = 0x03;

    step(vm);
    assert(vm->V[0] == 0x4);
    step(vm);
    assert(vm->V[0] == 0x3);
}

int main() {
    test_basic();
    return 0;
}
