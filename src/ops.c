#include "chip8.h"
#include "ops.h"

/*
 * Instruction: 0nnn
 * Description: Jump to a machine code routine at nnn. (Deprecated)
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opSYS(Chip8VM_t* vm, u16 addr) {
    debugs("Unsupported instruction 0nnn");
}

/*
 * Instruction: 00E0
 * Description: Clear the display.
 * @params  vm      The current state of the Virtual Machine
 */
void opCLS(Chip8VM_t* vm) {
    memset(vm->VRAM, 0, vm->sizeVRAM);
}

/*
 * Instruction: 00EE
 * Description: Return from a subroutine.
 * @params  vm      The current state of the Virtual Machine
 */
void opRET(Chip8VM_t* vm) {
    *vm->PC = vm->stack[*vm->SP];
    *vm->SP -= 1;
}

/*
 * Instruction: 1nnn
 * Description: Jump to location nnn.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opJP(Chip8VM_t* vm, u16 addr) {
    *vm->PC = addr;
}

/*
 * Instruction: 2nnn
 * Description: Call subroutine at nnn.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opCALL(Chip8VM_t* vm, u16 addr) {
    *vm->SP += 1;
    vm->stack[*vm->SP] = *vm->PC;
    *vm->PC = addr;
}

/*
 * Instruction: 3xkk
 * Description: Skip next instruction if the value of register Vx equals kk.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 *          value   The value (kk)
 */
void opSEValue(Chip8VM_t* vm, u8 reg, u8 value) {
    if (vm->V[reg] == value) {
        *vm->PC += 2;
    }
}

/*
 * Instruction: 4xkk
 * Description: Skip next instruction if the value of register Vx does not equal kk.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 *          value   The value (kk)
 */
void opSNEValue(Chip8VM_t* vm, u8 reg, u8 value) {
    if (vm->V[reg] != value) {
        *vm->PC += 2;
    }
}

/*
 * Instruction: 5xy0
 * Description: Skip next instruction if the value of register Vx equals the value
 *              of register Vy.
 * @params  vm      The current state of the Virtual Machine
 *          regX    Number (x) indicating a register Vx
 *          regY    Number (y) indicating a register Vy
 */
void opSEReg(Chip8VM_t* vm, u8 regX, u8 regY) {
    if (vm->V[regX] == vm->V[regY]) {
        *vm->PC += 2;
    }
}

/*
 * Instruction: 6xkk
 * Description: Set the value of register Vx to kk.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 *          value   The value (kk)
 */
void opLDValue(Chip8VM_t* vm, u8 reg, u8 value) {
    vm->V[reg] = value;
}

/*
 * Instruction: 7xkk
 * Description: Set the value of register Vx to the value of register Vx plus kk.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 *          value   The value (kk)
 */
void opADDValue(Chip8VM_t* vm, u8 reg, u8 value) {
    vm->V[reg] = vm->V[reg] + value;
}

/*
 * Instruction: 8xy0
 * Description: Set the value of register Vx to the value of register Vy.
 * @params  vm      The current state of the Virtual Machine
 *          regX    Number (x) indicating a register Vx
 *          regY    Number (y) indicating a register Vy
 */
void opLDReg(Chip8VM_t* vm, u8 regX, u8 regY) {
    vm->V[regX] = vm->V[regY];
}

/*
 * Instruction: 8xy1
 * Description: Set the value of register Vx to the bitwise OR of the values of
 *              registers Vx and Vy.
 * @params  vm      The current state of the Virtual Machine
 *          regX    Number (x) indicating a register Vx
 *          regY    Number (y) indicating a register Vy
 */
void opOR(Chip8VM_t* vm, u8 regX, u8 regY) {
    vm->V[regX] = vm->V[regX] | vm->V[regY];
}

/*
 * Instruction: 8xy2
 * Description: Set the value of register Vx to the bitwise AND of the values of
 *              registers Vx and Vy.
 * @params  vm      The current state of the Virtual Machine
 *          regX    Number (x) indicating a register Vx
 *          regY    Number (y) indicating a register Vy
 */
void opAND(Chip8VM_t* vm, u8 regX, u8 regY) {
    vm->V[regX] = vm->V[regX] & vm->V[regY];
}

/*
 * Instruction: 8xy3
 * Description: Set the value of register Vx to the bitwise exclusive OR of the
 *              values of registers Vx and Vy.
 * @params  vm      The current state of the Virtual Machine
 *          regX    Number (x) indicating a register Vx
 *          regY    Number (y) indicating a register Vy
 */
void opXOR(Chip8VM_t* vm, u8 regX, u8 regY) {
    vm->V[regX] = vm->V[regX] ^ vm->V[regY];
}

/*
 * Instruction: 8xy4
 * Description: Set the value of register Vx to the value of register Vx plus the
 *              value of register Vy and set the carry flag VF.
 * @params  vm      The current state of the Virtual Machine
 *          regX    Number (x) indicating a register Vx
 *          regY    Number (y) indicating a register Vy
 */
void opADDReg(Chip8VM_t* vm, u8 regX, u8 regY) {
    int a = vm->V[regX];
    int b = vm->V[regY];
    int c = a + b;
    vm->V[regX] = c;
    vm->V[0xF] = (c >> 8) & 0x1;
}

/*
 * Instruction: 8xy5
 * Description: Set the value of register Vx to the value of register Vx minus the
 *              value of register Vy and set the borrow flag VF.
 * @params  vm      The current state of the Virtual Machine
 *          regX    Number (x) indicating a register Vx
 *          regY    Number (y) indicating a register Vy
 */
void opSUB(Chip8VM_t* vm, u8 regX, u8 regY) {
    vm->V[0xF] = vm->V[regX] > vm->V[regY];
    vm->V[regX] = vm->V[regX] - vm->V[regY];
}

/*
 * Instruction: 8xy6
 * Description: Set the value of register Vx to the result of bit shifting the value
 *              of register Vx to the right and set the flag VF accordingly.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opSHR(Chip8VM_t* vm, u8 reg) {
    vm->V[0xF] = vm->V[reg] & 0x1;
    vm->V[reg] = vm->V[reg] >> 2;
}

/*
 * Instruction: 8xy7
 * Description: Set the value of register Vx to the value of register Vy minus the
 *              value of register Vx and set the borrow flag VF.
 * @params  vm      The current state of the Virtual Machine
 *          regX    Number (x) indicating a register Vx
 *          regY    Number (y) indicating a register Vy
 */
void opSUBN(Chip8VM_t* vm, u8 regX, u8 regY) {
    vm->V[0xF] = vm->V[regY] > vm->V[regX];
    vm->V[regX] = vm->V[regY] - vm->V[regX];
}

/*
 * Instruction: 8xyE
 * Description: Set the value of register Vx to the result of bit shifting the value
 *              of register Vx to the left and set the flag VF accordingly.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opSHL(Chip8VM_t* vm, u8 reg) {
    vm->V[0xF] = vm->V[reg] & 0x8;
    vm->V[reg] = vm->V[reg] << 2;
}

/*
 * Instruction: 9xy0
 * Description: Skip next instruction if the value of register Vx does not equal the
 *              value of register Vy.
 * @params  vm      The current state of the Virtual Machine
 *          regX    Number (x) indicating a register Vx
 *          regY    Number (y) indicating a register Vy
 */
void opSNEReg(Chip8VM_t* vm, u8 regX, u8 regY) {
    if (vm->V[regX] != vm->V[regY]) {
        *vm->PC += 2;
    }
}

/*
 * Instruction: Annn
 * Description: Set the value of register I to the address nnn.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opLDI(Chip8VM_t* vm, u16 addr) {
    *vm->I = addr;
}

/*
 * Instruction: Bnnn
 * Description: Jump to location nnn plus the value of register V0.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opJPV0(Chip8VM_t* vm, u16 addr) {
    *vm->PC = addr + vm->V[0];
}

/*
 * Instruction: Cxkk
 * Description: Set the value of register Vx to the bitwise AND of kk and a random
 *              number between 0 and 255.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 *          value   The value (kk)
 */
void opRND(Chip8VM_t* vm, u8 reg, u8 value) {
    srand(vm->seed);
    u8 n = rand() % 255;
    vm->seed = n;
    vm->V[reg] = n & value;
}

/*
 * Instruction: Dxyn
 * Description: Display an n-byte sprite starting at memory location I at coordinates
 *              (Vx, Vy) and set the collision flag VF.
 * @params  vm      The current state of the Virtual Machine
 *          regX    Number (x) indicating a register Vx
 *          regY    Number (y) indicating a register Vy
 *          size    The size of the sprite in bytes (n)
 */
void opDRW(Chip8VM_t* vm, u8 regX, u8 regY, u8 size) {
    u16 i = *vm->I;
    u8 x = vm->V[regX];
    u8 y = vm->V[regY];

    u8 erasedPixel = 0;
    for (u8 j = 0; j < size; j++) {
        u8 spriteByte = vm->RAM[i + j];

        u8 pixelY = (y + j) % 32;
        for (u8 k = 0; k < 8; k++) {
            u8 pixelX = (x + k) % 64;
            
            u8* ptr = vm->VRAM + 8 * pixelY + pixelX / 8;

            u8 byte = *ptr;
            *ptr = byte ^ (((spriteByte & (1 << (7 - k))) > 0) << (7 - pixelX % 8));
            
            // If collision vanished any pixel, erasedPixel will be 1
            erasedPixel &= (*ptr < byte);
        }
        vm->VRAM[8 * (y+j) * x] = vm->RAM[i+j];
    }

    vm->V[0xF] = erasedPixel;
}

/*
 * Instruction: Ex9E
 * Description: Skip next instruction if key with the value in register Vx is pressed.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opSKP(Chip8VM_t* vm, u8 reg) {
    if ((*vm->keys & reg) != 0) {
        *vm->PC += 2;
    }
}

/*
 * Instruction: ExA1
 * Description: Skip next instruction if key with the value in register Vx is not
 *              pressed.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opSKNP(Chip8VM_t* vm, u8 reg) {
    if ((*vm->keys & reg) == 0) {
        *vm->PC += 2;
    }
}

/*
 * Instruction: Fx07
 * Description: Set the value of register Vx to the delay timer value.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDRegDT(Chip8VM_t* vm, u8 reg) {
    vm->V[reg] = *vm->DT;
}

/*
 * Instruction: Fx0A
 * Description: Wait for a key press, store the number of register Vx into the wait register.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDRegKey(Chip8VM_t* vm, u8 reg) {
    vm->wait = 1;
    *vm->W = reg;
}

/*
 * Instruction: Fx15
 * Description: Set the delay timer to the value of register Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDDT(Chip8VM_t* vm, u8 reg) {
    *vm->DT = vm->V[reg];
}

/*
 * Instruction: Fx18
 * Description: Set the sound timer to the value of register Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDST(Chip8VM_t* vm, u8 reg) {
    *vm->ST = vm->V[reg];
}

/*
 * Instruction: Fx1E
 * Description: Set the value of register I to the value of register I plus the value
 *              of register Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opADDI(Chip8VM_t* vm, u8 reg) {
    *vm->I += vm->V[reg];
}

/*
 * Instruction: Fx29
 * Description: Set the value of register I to the location of the sprite corresponding
 *              to the value of register Vx. Each hex sprite is five bytes long.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDSprite(Chip8VM_t* vm, u8 reg) {
    *vm->I = vm->hexes[vm->V[reg] * 5];
}

/*
 * Instruction: Fx33
 * Description: Store the Binary Coded Decimal representation of Vx in memory locations
 *              I, I+1, and I+2.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDBCD(Chip8VM_t* vm, u8 reg) {
    u16 i = *vm->I;
    vm->RAM[i] = i / 100;
    vm->RAM[i+1] = (i / 10) % 10;
    vm->RAM[i+2] = i % 10;
}

/*
 * Instruction: Fx55
 * Description: Store the values of registers V0 through Vx in memory starting at
 *              location I.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDRegs(Chip8VM_t* vm, u8 reg) {
    u16 i = *vm->I;
    for (u8 j = 0; j <= reg; j++) {
        vm->RAM[i + j] = vm->V[j];
    }
}

/*
 * Instruction: Fx65
 * Description: Store the value of memory starting at location I into registers V0
 *              through Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDMem(Chip8VM_t* vm, u8 reg) {
    u16 i = *vm->I;
    for (u8 j = 0; j <= reg; j++) {
        vm->V[j] = vm->RAM[i + j];
    }
}
