#define _CRT_SECURE_NO_DEPRECATE
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "chip8.h"
#include "ops.h"

void PyInit_libchip_gr8() {}

/**
 * Performs additional changes to the VM after an instruction has occured.
 * 
 * @params vm the vm
 */
void preStep(Chip8VM_t * vm) {
    // Reset diff flags
    vm->diffSize  = 0;
    vm->diffClear = 0;
    // Increment the clock
    vm->clock    += 1;
}

/**
 * Performs additional changes to the VM after an instruction has occured.
 * 
 * @params vm the vm
 */
void postStep(Chip8VM_t* vm) {
    // Update timers at 60Hz
    if (vm->clock % vm->freq == 0) {
        // Decrement DT and ST if positive
        if (vm->DT > 0) { vm->DT -= 1; }
        if (vm->ST > 0) { vm->ST -= 1; }
    }
}

/**
 * Sets the input registers on the VM.
 * 
 * @params vm the vm 
 *         keymask a mask of keys currently down
 */
void input(Chip8VM_t* vm, u16 keymask) {
    vm->K = keymask;
    if (keymask && vm->wait) {
        u8 decodedKeymask = 0;
        // Decode keymask, get most significant bit key
        while (keymask >>= 1) { decodedKeymask++; }
        // Assign to wait register V[W]
        vm->V[vm->W] = decodedKeymask;
        // Stop waiting
        vm->wait = 0;
    }
}

/**
 * @returns a SHARED_LIBRARY_ID to ensure that the library has been loaded
 *          correctly.
 */
int helloSharedLibrary() {
    return SHARED_LIBRARY_ID;
}

/**
 * Initializes a VM instance to a valid initial sate. This is the only way a 
 * Chip-8 vm should be instantiated.
 * 
 * @params vm the vm to intialize
 */
void initVM(Chip8VM_t* vm, u8 freq) {
    debugf("vm pointer: %p\n", (void *) vm);
    // memset(vm->RAM, 0, 0xFFF);
    vm->freq    = freq;
    vm->PC      = PROGRAM_SPACE_START;
    vm->I       = PROGRAM_SPACE_START;

    // Initialize hexsprites
    STORE_HEXSPRITE(vm->hexes, 0,  HEXSPRITE_0);
    STORE_HEXSPRITE(vm->hexes, 1,  HEXSPRITE_1);
    STORE_HEXSPRITE(vm->hexes, 2,  HEXSPRITE_2);
    STORE_HEXSPRITE(vm->hexes, 3,  HEXSPRITE_3);
    STORE_HEXSPRITE(vm->hexes, 4,  HEXSPRITE_4);
    STORE_HEXSPRITE(vm->hexes, 5,  HEXSPRITE_5);
    STORE_HEXSPRITE(vm->hexes, 6,  HEXSPRITE_6);
    STORE_HEXSPRITE(vm->hexes, 7,  HEXSPRITE_7);
    STORE_HEXSPRITE(vm->hexes, 8,  HEXSPRITE_8);
    STORE_HEXSPRITE(vm->hexes, 9,  HEXSPRITE_9);
    STORE_HEXSPRITE(vm->hexes, 10, HEXSPRITE_A);
    STORE_HEXSPRITE(vm->hexes, 11, HEXSPRITE_B);
    STORE_HEXSPRITE(vm->hexes, 12, HEXSPRITE_C);
    STORE_HEXSPRITE(vm->hexes, 13, HEXSPRITE_D);
    STORE_HEXSPRITE(vm->hexes, 14, HEXSPRITE_E);
    STORE_HEXSPRITE(vm->hexes, 15, HEXSPRITE_F);
}

/**
 * Steps a VM 1 clock cycle. 
 * 
 * @params vm the vm
 */
void step(Chip8VM_t* vm) {
    preStep(vm);
    if (!vm->wait) {
        word_t opcode = fetch(vm);
        Instruction_t instruction = decode(opcode);
        evaluate(vm, instruction, opcode);
    }
    postStep(vm);
}

/**
 * Fetches the next instruction then increments the program counter by 2.
 * 
 * @params  vm the vm
 * @returns    the next 
 */
word_t fetch(Chip8VM_t* vm) {
    word_t msb = vm->RAM[vm->PC] << 8;
    word_t lsb = vm->RAM[vm->PC + 1];
    vm->PC += 2;
    return msb + lsb;
}

/**
 * Decodes and dispatches the next opcode performing the appropraite action and
 * changing the VM state.
 * 
 * @params vm     the vm
 *         opcode the instruction opcode
 */
Instruction_t decode(word_t opcode) {
    word_t msn = opcode >> 12;
    word_t lsn = opcode & 0xF;
    switch (msn) {
        case 0x00: {
            // When the instruction starts with zero
            // there are only three instructions
            // and the SYS instruction is not used
            // in modern systems.
            if (opcode == 0x00e0) {
                return CLEAR;
            }
            else if (opcode == 0x00ee) {
                return RET;
            }
            else {
                return SYS;
            }
            break;
        }
        case 0x01: {
            return JUMP;
        }
        case 0x02: {
            return CALL;
        }
        case 0x03: {
            return SKIPE;
        }
        case 0x04: {
            return SKIPN;
        }
        case 0x05: {
            return SKIPR;
        }
        case 0x06: {
            return LOAD;
        }
        case 0x07: {
            return ADD;
        }
        case 0x08: {
            if (lsn == 0x0) {
                return LOADR;
            }
            else if (lsn == 0x1) {
                return OR;
            }
            else if (lsn == 0x2) {
                return AND;
            }
            else if (lsn == 0x3) {
                return XOR;
            }
            else if (lsn == 0x4) {
                return ADDR;
            }
            else if (lsn == 0x5) {
                return SUB;
            }
            else if (lsn == 0x6) {
                return SHIFTREG;
            }
            else if (lsn == 0x7) {
                return SUBN;
            }
            else if (lsn == 0xE) {
                return SHIFTL;
            }
            else {
                debugs("Encountered an invalid instruction.");
                return INVALID_INSTRUCTION;
            }
        }
        case 0x09: {
            return SKIPNR;
        }
        case 0x0A: {
            return LOADADDR;
        }
        case 0x0B: {
            return JUMPADDR;
        }
        case 0x0C: {
            return RANDOM;
        }
        case 0x0D: {
            return DRAW;
        }
        case 0x0E: {
            if (lsn == 0xE) {
                return SKIP;
            }
            else {
                return SKIPNP;
            }
        }
        case 0x0F: {
            word_t sub = opcode & 0xFF;
            if (sub == 0x7) {
                return LDRDT;
            }
            else if (sub == 0xA) {
                return LDRK;
            }
            else if (sub == 0x15) {
                return LDDT;
            }
            else if (sub == 0x18) {
                return LDST;
            }
            else if (sub == 0x1E) {
                return ADDI;
            }
            else if (sub == 0x29) {
                return LDSPRI;
            }
            else if (sub == 0x33) {
                return LDBCD;
            }
            else if (sub == 0x55) {
                return LDREGS;
            }
            else if (sub == 0x65) {
                return LDMEM;
            }
            else {
                debugs("Encountered an invalid instruction.");
                return INVALID_INSTRUCTION;
            }
        }
        default: {
            debugf("Impossible most signifigant nibble: %x !", msn);
            return INVALID_INSTRUCTION;
        }
    }
}

/**
 * Evaluates the opcode and extracts the arguements,
 * then calls the appropriate system function.
 * 
 * @params vm the vm 
 *         inst the current instruction
 *         opcode the current opcode
 */
void evaluate(Chip8VM_t* vm, Instruction_t inst, word_t opcode) {
    switch (inst) {
        case SYS: {
            // NOP
            break;
        }
        case CLEAR: {
            opCLS(vm);
            break;
        }
        case RET: {
            opRET(vm);
            break;
        }
        case JUMP: {
            opJP(vm, getValue12Bit(opcode));
            break;
        }
        case CALL: {
            opCALL(vm, getValue12Bit(opcode));
            break;
        }
        case SKIPE: {
            opSEValue(vm, getRegisterX(opcode), getValue8Bit(opcode));
            break;
        }
        case SKIPN: {
            opSNEValue(vm, getRegisterX(opcode), getValue8Bit(opcode));
            break;
        }
        case SKIPR: {
            opSEReg(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case LOAD: {
            opLDValue(vm, getRegisterX(opcode), getValue8Bit(opcode));
            break;
        }
        case ADD: {
            opADDValue(vm, getRegisterX(opcode), getValue8Bit(opcode));
            break;
        }
        case LOADR: {
            opLDReg(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case OR: {
            opOR(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case AND: {
            opAND(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case XOR: {
            opXOR(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case ADDR: {
            opADDReg(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case SUB: {
            opSUB(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case SHIFTREG: {
            opSHR(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case SUBN: {
            opSUBN(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case SHIFTL: {
            opSHL(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case SKIPNR: {
            opSNEReg(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case LOADADDR: {
            opLDI(vm, getValue12Bit(opcode));
            break;
        }
        case JUMPADDR: {
            opJPV0(vm, getValue12Bit(opcode));
            break;
        }
        case RANDOM: {
            opRND(vm, getRegisterX(opcode), getValue8Bit(opcode));
            break;
        }
        case DRAW: {
            opDRW(vm, getRegisterX(opcode), getRegisterY(opcode), getValue4Bit(opcode));
            break;
        }
        case SKIP: {
            opSKP(vm, getRegisterX(opcode));
            break;
        }
        case SKIPNP: {
            opSKNP(vm, getRegisterX(opcode));
            break;
        }
        case LDRDT: {
            opLDRegDT(vm, getRegisterX(opcode));
            break;
        }
        case LDRK: {
            opLDRegKey(vm, getRegisterX(opcode));
            break;
        }
        case LDDT: {
            opLDDT(vm, getRegisterX(opcode));
            break;
        }
        case LDST: {
            opLDST(vm, getRegisterX(opcode));
            break;
        }
        case ADDI: {
            opADDI(vm, getRegisterX(opcode));
            break;
        }
        case LDSPRI: {
            opLDSprite(vm, getRegisterX(opcode));
            break;
        }
        case LDBCD: {
            opLDBCD(vm, getRegisterX(opcode));
            break;
        }
        case LDREGS: {
            opLDRegs(vm, getRegisterX(opcode));
            break;
        }
        case LDMEM: {
            opLDMem(vm, getRegisterX(opcode));
            break;
        }
        default: {
            debugf("Invalid instruction or instruction not implemented: %d %x\n", inst, opcode);
            break;
        }
    }
}

u8 getRegisterX(word_t opcode) {
    return (opcode & 0x0F00) >> 8;
}

u8 getRegisterY(word_t opcode) {
    return (opcode & 0x00F0) >> 4;
}

u8 getValue8Bit(word_t opcode) {
    return opcode & 0x00FF;
}

u16 getValue12Bit(word_t opcode) {
    return opcode & 0x0FFF;
}

u8 getValue4Bit(word_t opcode) {
    return opcode & 0xF;
}

/**
 * Load a ROM from a file into the vm.
 * 
 * @params vm       the vm
 *         filePath the path to the ROM
 * @returns         0 on failure
 */
int loadROM(Chip8VM_t* vm, char* filePath) {
    FILE* file = fopen(filePath, "rb");
    if (file == NULL) {
        debugf("Failed to load ROM %s\n", filePath);
        return 0;
    } 

    fseek(file, 0, SEEK_END);
    u32 len = ftell(file);
    rewind(file);
    if (len > 0x1000- PROGRAM_SPACE_START) {
        len = 0x1000 - PROGRAM_SPACE_START;
    }
    debugf("ROM Length: %u\n", len);

    fread(vm->RAM + PROGRAM_SPACE_START, len, 1, file);
    fclose(file);
    debugs("Succesfully loaded ROM file.\n");
    // Reset PC and SP (more? TODO)
    vm->PC = PROGRAM_SPACE_START;
    vm->SP = 0;
    return 1;
}
