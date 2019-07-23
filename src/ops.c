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
    vm->diffClear = 1;
    memset(vm->VRAM, 0, 0x100);
}

/*
 * Instruction: 00EE
 * Description: Return from a subroutine.
 * @params  vm      The current state of the Virtual Machine
 */
void opRET(Chip8VM_t* vm) {
    vm->PC  = vm->stack[vm->SP];
    vm->SP -= 1;
}

/*
 * Instruction: 1nnn
 * Description: Jump to location nnn.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opJP(Chip8VM_t* vm, u16 addr) {
    vm->PC = addr;
}

/*
 * Instruction: 2nnn
 * Description: Call subroutine at nnn.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opCALL(Chip8VM_t* vm, u16 addr) {
    vm->SP += 1;
    vm->stack[vm->SP] = vm->PC;
    vm->PC = addr;
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
        vm->PC += 2;
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
        vm->PC += 2;
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
        vm->PC += 2;
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
    vm->V[0xF]  = vm->V[regX] >= vm->V[regY];
    vm->V[regX] = vm->V[regX] - vm->V[regY];
}

/*
 * Instruction: 8xy6
 * Description: Default behaviour is to shift the value of register Vx to the right,
 *              store the result in Vx, and set the flag VF accordingly. When a ROM
 *              has the SHIFT_QUIRK flag set, the behaviour is to shift the value of
 *              register Vy to the right, store the result in Vx, and set the flag
 *              VF accordingly.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opSHR(Chip8VM_t* vm, u8 regX, u8 regY) {
    if (!(vm->quirks & SHIFT_QUIRK)) {
        regY = regX;
    }
    vm->V[0xF]  = vm->V[regY] & 0x1;
    vm->V[regX] = vm->V[regY] >> 1;
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
    vm->V[0xF]  = vm->V[regY] >= vm->V[regX];
    vm->V[regX] = vm->V[regY] - vm->V[regX];
}

/*
 * Instruction: 8xyE
 * Description: Default behaviour is to shift the value of register Vx to the left,
 *              store the result in Vx, and set the flag VF accordingly. When a ROM
 *              has the SHIFT_QUIRK flag set, the behaviour is to shift the value of
 *              register Vy to the left, store the result in Vx, and set the flag
 *              VF accordingly.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opSHL(Chip8VM_t* vm, u8 regX, u8 regY) {
    if (!(vm->quirks & SHIFT_QUIRK)) {
        regY = regX;
    }
    vm->V[0xF]  = vm->V[regY] & 0x8;
    vm->V[regX] = vm->V[regY] << 1;
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
        vm->PC += 2;
    }
}

/*
 * Instruction: Annn
 * Description: Set the value of register I to the address nnn.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opLDI(Chip8VM_t* vm, u16 addr) {
    vm->I = addr;
}

/*
 * Instruction: Bnnn
 * Description: Jump to location nnn plus the value of register V0.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opJPV0(Chip8VM_t* vm, u16 addr) {
    vm->PC = addr + vm->V[0];
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

    u16 i = vm->I;
    u8 x  = vm->diffX = vm->V[regX];
    u8 y  = vm->diffY = vm->V[regY];

    vm->diffSize = size;
    vm->diffSkip = 1;
    vm->V[0xF]   = 0;

    // for each row of the sprite
    for (u8 j = 0; j < size; j ++) {
        // get the sprite data byte
        u8 spriteByte = vm->RAM[i + j];

        // if the row will be off the bottom of the screen, don't draw it
        if (vm->quirks & DRAW_QUIRK) {
            if ((y + j) >= 32) break;
        }

        // calculate the intended coordinates
        u8 row = (y + j) % 32;
        u8 col = x % 64;

        // calculate corresponding location in VRAM
        u16 bit          = ((row * 64) + col);
        u16 firstByte    = bit / 8;
        u16 secondByte   = col >= 56 ? (row * 8) : firstByte + 1;
        u8 bitOffset     = bit % 8;
        u8 leftoverBits  = 8 - bitOffset;

        // check bounds for safety
        if (secondByte > 0x100) {
            debugs("Tried to draw outside VRAM!");
            return;
        }

        // get the existing VRAM data for the intended location
        u8 oldVRAMData = (vm->VRAM[firstByte] << bitOffset) | (vm->VRAM[secondByte] >> leftoverBits);

        // compare to set the collision flag
        if (oldVRAMData & spriteByte) {
            vm->V[0xF] = 1;
        }

        // Set skip flag
        if (oldVRAMData ^ spriteByte) {
            vm->diffSkip = 0;
        }

        // set VRAM memory
        vm->VRAM[firstByte]  ^= (spriteByte >> bitOffset);
        vm->VRAM[secondByte] ^= (spriteByte << leftoverBits);
    }
}

/*
 * Instruction: Ex9E
 * Description: Skip next instruction if key with the value in register Vx is pressed.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opSKP(Chip8VM_t* vm, u8 reg) {
    if ((vm->K >> vm->V[reg]) & 1) {
        vm->PC += 2;
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
    if (!((vm->K >> vm->V[reg]) & 1)) {
        vm->PC += 2;
    }
}

/*
 * Instruction: Fx07
 * Description: Set the value of register Vx to the delay timer value.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDRegDT(Chip8VM_t* vm, u8 reg) {
    vm->V[reg] = vm->DT;
}

/*
 * Instruction: Fx0A
 * Description: Wait for a key press, store the number of register Vx into the wait register.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDRegKey(Chip8VM_t* vm, u8 reg) {
    vm->wait = 1;
    vm->W = reg;
}

/*
 * Instruction: Fx15
 * Description: Set the delay timer to the value of register Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDDT(Chip8VM_t* vm, u8 reg) {
    vm->DT = vm->V[reg];
}

/*
 * Instruction: Fx18
 * Description: Set the sound timer to the value of register Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDST(Chip8VM_t* vm, u8 reg) {
    vm->ST = vm->V[reg];
}

/*
 * Instruction: Fx1E
 * Description: Set the value of register I to the value of register I plus the value
 *              of register Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opADDI(Chip8VM_t* vm, u8 reg) {
    vm->I += vm->V[reg];
}

/*
 * Instruction: Fx29
 * Description: Set the value of register I to the location of the sprite corresponding
 *              to the value of register Vx. Each hex sprite is five bytes long.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDSprite(Chip8VM_t* vm, u8 reg) {
    vm->I = vm->V[reg] * 5;
}

/*
 * Instruction: Fx33
 * Description: Store the Binary Coded Decimal representation of Vx in memory locations
 *              I, I+1, and I+2.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDBCD(Chip8VM_t* vm, u8 reg) {
    u16 i = vm->I;
    u8  x = vm->V[reg];
    vm->RAM[i] = x / 100;
    vm->RAM[i+1] = (x / 10) % 10;
    vm->RAM[i+2] = x % 10;
}

/*
 * Instruction: Fx55
 * Description: Store the value of memory starting at location I into registers V0
 *              through Vx. Default behaviour is to leave the value of I unaffected.
 *              When a ROM has the LOAD_QUIRK flag set, the behaviour is to increment
 *              the value of I.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDRegs(Chip8VM_t* vm, u8 reg) {
    u16 i = vm->I;
    u8 j;
    for (j = 0; j <= reg; j++) {
        vm->RAM[i + j] = vm->V[j];
    }
    if (vm->quirks & LOAD_QUIRK) {
        vm->I = i + j;
    }
}

/*
 * Instruction: Fx65
 * Description: Store the value of memory starting at location I into registers V0
 *              through Vx. Default behaviour is to leave the value of I unaffected.
 *              When a ROM has the LOAD_QUIRK flag set, the behaviour is to increment
 *              the value of I.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDMem(Chip8VM_t* vm, u8 reg) {
    u16 i = vm->I;
    u8 j;
    for (j = 0; j <= reg; j++) {
        vm->V[j] = vm->RAM[i + j];
    }
    if (vm->quirks & LOAD_QUIRK) {
        vm->I = i + j;
    }
}
