#include "chip8.h"
#include "ops.h"

/*
 * Instruction: 0nnn
 * Description: Jump to a machine code routine at nnn.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opSYS(Chip8VM_t* vm, u16 addr) {
    // TODO
    return;
}

/*
 * Instruction: 00E0
 * Description: Clear the display.
 * @params  vm      The current state of the Virtual Machine
 */
void opCLS(Chip8VM_t* vm) {
    // TODO
    return;
}

/*
 * Instruction: 00EE
 * Description: Return from a subroutine.
 * @params  vm      The current state of the Virtual Machine
 */
void opRET(Chip8VM_t* vm) {
    // TODO
    return;
}

/*
 * Instruction: 1nnn
 * Description: Jump to location nnn.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opJP(Chip8VM_t* vm, u16 addr) {
    // TODO
    return;
}

/*
 * Instruction: 2nnn
 * Description: Call subroutine at nnn.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opCALL(Chip8VM_t* vm, u16 addr) {
    // TODO
    return;
}

/*
 * Instruction: 3xkk
 * Description: Skip next instruction if the value of register Vx equals kk.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 *          value   The value (kk)
 */
void opSEValue(Chip8VM_t* vm, u8 reg, u8 value) {
    // TODO
    return;
}

/*
 * Instruction: 4xkk
 * Description: Skip next instruction if the value of register Vx does not equal kk.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 *          value   The value (kk)
 */
void opSNEValue(Chip8VM_t* vm, u8 reg, u8 value) {
    // TODO
    return;
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
    // TODO
    return;
}

/*
 * Instruction: 6xkk
 * Description: Set the value of register Vx to kk.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 *          value   The value (kk)
 */
void opLDValue(Chip8VM_t* vm, u8 reg, u8 value) {
    // TODO
    return;
}

/*
 * Instruction: 7xkk
 * Description: Set the value of register Vx to the value of register Vx plus kk.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 *          value   The value (kk)
 */
void opADDValue(Chip8VM_t* vm, u8 reg, u8 value) {
    // TODO
    return;
}

/*
 * Instruction: 8xy0
 * Description: Set the value of register Vx to the value of register Vy.
 * @params  vm      The current state of the Virtual Machine
 *          regX    Number (x) indicating a register Vx
 *          regY    Number (y) indicating a register Vy
 */
void opLDReg(Chip8VM_t* vm, u8 regX, u8 regY) {
    // TODO
    return;
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
    // TODO
    return;
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
    // TODO
    return;
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
    // TODO
    return;
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
    // TODO
    return;
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
    // TODO
    return;
}

/*
 * Instruction: 8xy6
 * Description: Set the value of register Vx to the result of bit shifting the value
 *              of register Vx to the right and set the flag VF accordingly.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opSHR(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
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
    // TODO
    return;
}

/*
 * Instruction: 8xyE
 * Description: Set the value of register Vx to the result of bit shifting the value
 *              of register Vx to the left and set the flag VF accordingly.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opSHL(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
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
    // TODO
    return;
}

/*
 * Instruction: Annn
 * Description: Set the value of register I to the value nnn.
 * @params  vm      The current state of the Virtual Machine
 *          value   The value (nnn)
 */
void opLDI(Chip8VM_t* vm, u8 value) {
    // TODO
    return;
}

/*
 * Instruction: Bnnn
 * Description: Jump to location nnn plus the value of register V0.
 * @params  vm      The current state of the Virtual Machine
 *          addr    The address (nnn)
 */
void opJPV0(Chip8VM_t* vm, u8 addr) {
    // TODO
    return;
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
    // TODO
    return;
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
    // TODO
    return;
}

/*
 * Instruction: Ex9E
 * Description: Skip next instruction if key with the value in register Vx is pressed.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opSKP(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
}

/*
 * Instruction: ExA1
 * Description: Skip next instruction if key with the value in register Vx is not
 *              pressed.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opSKNP(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
}

/*
 * Instruction: Fx07
 * Description: Set the value of register Vx to the delay timer value.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDRegDT(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
}

/*
 * Instruction: Fx0A
 * Description: Wait for a key press, store the value of the key in register Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDRegKey(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
}

/*
 * Instruction: Fx15
 * Description: Set the delay timer to the value of register Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDDT(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
}

/*
 * Instruction: Fx18
 * Description: Set the sound timer to the value of register Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDST(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
}

/*
 * Instruction: Fx1E
 * Description: Set the value of register I to the value of register I plus the value
 *              of register Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opADDI(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
}

/*
 * Instruction: Fx29
 * Description: Set the value of register I to the location of the sprite corresponding
 *              to the value of register Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDSprite(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
}

/*
 * Instruction: Fx33
 * Description: Store the Binary Coded Decimal representation of Vx in memory locations
 *              I, I+1, and I+2.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDBCD(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
}

/*
 * Instruction: Fx55
 * Description: Store the values of registers V0 through Vx in memory starting at
 *              location I.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDRegs(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
}

/*
 * Instruction: Fx65
 * Description: Store the value of memory starting at location I into registers V0
 *              through Vx.
 * @params  vm      The current state of the Virtual Machine
 *          reg     Number (x) indicating a register Vx
 */
void opLDMem(Chip8VM_t* vm, u8 reg) {
    // TODO
    return;
}