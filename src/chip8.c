#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "chip8.h"
#include "ops.h"

void evaluate(Chip8VM_t* vm, Instruction_t inst, word_t opcode) {
    switch (inst) {
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
            opSHR(vm, getRegisterX(opcode));
            break;
        }
        case SUBN: {
            opSUBN(vm, getRegisterX(opcode), getRegisterY(opcode));
            break;
        }
        case SHIFTL: {
            opSHL(vm, getRegisterX(opcode));
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
            debugs("Invalid instruction or instruction not implemented");
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

u8 getValue12Bit(word_t opcode) {
    return opcode & 0x0FFF;
}

u8 getValue4Bit(word_t opcode) {
    return opcode & 0xF;
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
void initVM(Chip8VM_t* vm) {
    // Initialize constant fields
    vm->sizeRAM   = RAM_SIZE;
    vm->sizeVRAM  = VRAM_SIZE;
    vm->sizeStack = LEN_STACK * 2;
    vm->seed = 0;
    vm->wait = 0;
    vm->clock = 0;

    // Initialize allocated fields
    vm->RAM   = malloc(vm->sizeRAM);
    vm->VRAM  = malloc(vm->sizeVRAM);

    // Initialize pointers
    vm->SP    = STACK_POINTER(vm->RAM);
    vm->PC    = PROGRAM_COUNTER(vm->RAM);
    vm->I     = ADDRESS_REGISTER(vm->RAM);
    vm->V     = GENERAL_REGISTERS(vm->RAM);
    vm->DT    = DELAY_TIMER(vm->RAM);
    vm->ST    = SOUND_TIMER(vm->RAM);
    vm->keys  = KEY_IO_REGISTERS(vm->RAM);
    vm->W     = WAIT_REGISTER(vm->RAM);

    vm->stack = STACK_START(vm->RAM);
    vm->hexes = HEXSPRITE_START(vm->RAM);

    *vm->SP   = 0;
    *vm->PC   = PROGRAM_SPACE_START;
    *vm->I    = PROGRAM_SPACE_START;
    *vm->DT   = 0;
    *vm->ST   = 0;
    *vm->keys = 0;
    *vm->W    = 0;

    // Initialize hexsprites
    // TODO: Condense hexsprites?
    STORE_HEXSPRITE(vm->hexes, 0, HEXSPRITE_0);
    STORE_HEXSPRITE(vm->hexes, 1, HEXSPRITE_1);
    STORE_HEXSPRITE(vm->hexes, 2, HEXSPRITE_2);
    STORE_HEXSPRITE(vm->hexes, 3, HEXSPRITE_3);
    STORE_HEXSPRITE(vm->hexes, 4, HEXSPRITE_4);
    STORE_HEXSPRITE(vm->hexes, 5, HEXSPRITE_5);
    STORE_HEXSPRITE(vm->hexes, 6, HEXSPRITE_6);
    STORE_HEXSPRITE(vm->hexes, 7, HEXSPRITE_7);
    STORE_HEXSPRITE(vm->hexes, 8, HEXSPRITE_8);
    STORE_HEXSPRITE(vm->hexes, 9, HEXSPRITE_9);
    STORE_HEXSPRITE(vm->hexes, 10, HEXSPRITE_A);
    STORE_HEXSPRITE(vm->hexes, 11, HEXSPRITE_B);
    STORE_HEXSPRITE(vm->hexes, 12, HEXSPRITE_C);
    STORE_HEXSPRITE(vm->hexes, 13, HEXSPRITE_D);
    STORE_HEXSPRITE(vm->hexes, 14, HEXSPRITE_E);
    STORE_HEXSPRITE(vm->hexes, 15, HEXSPRITE_F);

    // Initialize stack
    for(u8 i = 0; i < LEN_STACK; i++) {
        vm->stack[i] = 0;
    }
}

/**
 * Deallocates a VM instance. The VM instance should NOT be accessed after
 * being passed to this function.
 * 
 * @params vm the vm to deallocate
 */
void freeVM(Chip8VM_t* vm) {
    // #TODO perform any other necessary cleanup (eg. closing ROM file)
    /* if (vm->ROM != NULL) {
        unloadROM(vm);
    }*/
    free(vm->VRAM);
    free(vm->RAM);
    free(vm);
}

/**
 * Steps a VM 1 clock cycle. 
 * 
 * @params vm the vm
 */
void step(Chip8VM_t* vm) {
    // This code is questionable (should probably be factored out)
    if (vm->wait) {
        if (*vm->keys) {
            vm->wait = 0;
            int keys = *vm->keys;
            int key  = 0;
            while (keys != 0) {
                key = key >> 1;
                key++;
            }
            vm->V[*vm->W] = key;
        } else {
            return;
        }
    }
    word_t opcode = fetch(vm);
    Instruction_t instruction = decode(opcode);
    evaluate(vm, instruction, opcode);
    update(vm);
}

/**
 * Fetches the next instruction then increments the program counter by 2.
 * 
 * @params  vm the vm
 * @returns    the next 
 */
word_t fetch(Chip8VM_t* vm) {
    word_t msb = vm->RAM[*vm->PC] << 8;    
    word_t lsb = vm->RAM[*vm->PC + 1];    
    *vm->PC += 2;
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
            return SKIPNP;
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
                return SKIPNR;
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
            else if (sub == 0x66) {
                return LDMEM;
            }
            else {
                debugs("Invalid instruction.");
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
 * Performs additional changes to the VM that are not covered by instruction
 * decode and dispatch.
 * 
 * @params vm the vm
 */
void update(Chip8VM_t* vm) {
    // Decrement DT and ST if positive
    if (*vm->DT > 0) { *vm->DT -= 1; }
    if (*vm->ST > 0) { *vm->ST -= 1; }
}

/**
 * Load a ROM from a file into the vm.
 * 
 * @params vm       the vm
 *         filePath the path to the ROM
 * @returns         0 on failure
 */
int loadROM(Chip8VM_t* vm, char* filePath) {
    FILE* file = fopen(filePath, "r");
    if (file == NULL) {
        debugf("failed to load ROm %s\n", filePath);
        return 0;
    } 
    fread(vm->RAM + 0x200, vm->sizeRAM - 0x200, 1, file);
    fclose(file);
    debugs("Succesfully loaded ROM file.\n");
    // Reset PC and SP (more? TODO)
    *vm->PC = 0x200;
    *vm->SP = 0;
    return 1;
}
