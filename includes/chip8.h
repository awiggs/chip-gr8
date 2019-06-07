#pragma once

#ifndef CHIP8_H
#define CHIP8_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "pinttypes.h"
#include "autogen_Chip8VMStruct.h"
#include "ops.h"
#include "debug.h"
#include "instructions.h"

#define PROGRAM_SPACE_START         0x200

#define RAM_SIZE                    0x1000
#define VRAM_SIZE                   (64 / 8) * 32

#define LEN_STACK                   16

#define HEXSPRITE_BASE_OFFSET       0
#define HEXSPRITE_START(_ram)       (_ram + HEXSPRITE_BASE_OFFSET)

#define HEXSPRITE_0                 0xF999F
#define HEXSPRITE_1                 0x26227
#define HEXSPRITE_2                 0xF1F8F
#define HEXSPRITE_3                 0xF1F1F
#define HEXSPRITE_4                 0x99F11
#define HEXSPRITE_5                 0xF8F1F
#define HEXSPRITE_6                 0xF8F9F
#define HEXSPRITE_7                 0xF1244
#define HEXSPRITE_8                 0xF9F9F
#define HEXSPRITE_9                 0xF9F1F
#define HEXSPRITE_A                 0xF9F99
#define HEXSPRITE_B                 0xE9E9E
#define HEXSPRITE_C                 0xF888F
#define HEXSPRITE_D                 0xE999E
#define HEXSPRITE_E                 0xF8F8F
#define HEXSPRITE_F                 0xF8F88

// To avoid defining very large int literals, interlaces hexsprite int literal with 0s
// such that 0x11111 becomes 0x1010101010 then stores each byte to arr
#define STORE_HEXSPRITE(_arr, _ind, _spr)   SAFE_MACRO( \
                                                u32 _hex = _spr; \
                                                for(u8 _i = 0; _i < 5; _i++){ \
                                                    *(_arr + (_ind * 5) + _i) = ((_hex >> ((4 - _i) * 4) & 0xF) << 4); \
                                                } \
                                            )

#define REGISTER_BASE_OFFSET        80

#define ALL_REGISTERS_SIZE          26
// The following are offset from REGISTER_BASE_OFFSET
#define STACK_POINTER_OFFSET        0
#define PROGRAM_COUNTER_OFFSET      1
#define ADDRESS_REGISTER_OFFSET     3
#define GENERAL_REGISTERS_OFFSET    5
#define DELAY_TIMER_OFFSET          21
#define SOUND_TIMER_OFFSET          22
#define KEY_IO_REGISTERS_OFFSET     23
#define WAIT_REGISTER_OFFSET        25
// End offsets from REGISTER_BASE_OFFSET

#define REGISTER_BASE(_ram)         (_ram + REGISTER_BASE_OFFSET)

#define STACK_POINTER(_ram)         ((void *) (REGISTER_BASE(_ram) + STACK_POINTER_OFFSET))
#define PROGRAM_COUNTER(_ram)       ((void *) (REGISTER_BASE(_ram) + PROGRAM_COUNTER_OFFSET))
#define ADDRESS_REGISTER(_ram)      ((void *) (REGISTER_BASE(_ram) + ADDRESS_REGISTER_OFFSET))
#define GENERAL_REGISTERS(_ram)     ((void *) (REGISTER_BASE(_ram) + GENERAL_REGISTERS_OFFSET))
#define DELAY_TIMER(_ram)           ((void *) (REGISTER_BASE(_ram) + DELAY_TIMER_OFFSET))
#define SOUND_TIMER(_ram)           ((void *) (REGISTER_BASE(_ram) + SOUND_TIMER_OFFSET))
#define KEY_IO_REGISTERS(_ram)      ((void *) (REGISTER_BASE(_ram) + KEY_IO_REGISTERS_OFFSET))
#define WAIT_REGISTER(_ram)         ((void *) (REGISTER_BASE(_ram) + WAIT_REGISTER_OFFSET))

#define STACK_BASE_OFFSET           REGISTER_BASE_OFFSET + ALL_REGISTERS_SIZE
#define STACK_START(_ram)           ((void *) (_ram + STACK_BASE_OFFSET))


typedef u16 word_t;

#include "autogen_Chip8VMStruct.h"

#define SHARED_LIBRARY_ID 0xAFBFCF;
/**
 * @returns a SHARED_LIBRARY_ID to ensure that the library has been loaded
 *          correctly.
 */
int helloSharedLibrary();

/**
 * Initializes a VM instance to a valid initial sate. This is the only way a 
 * Chip-8 vm should be instantiated.
 * 
 * @params vm the vm to intialize
 */
void initVM(Chip8VM_t* vm);

/**
 * Deallocates a VM instance. The VM instance should NOT be accessed after
 * being passed to this function.
 * 
 * @params vm the vm to deallocate
 */
void freeVM(Chip8VM_t* vm); 

/**
 * Steps a VM 1 clock cycle. 
 * 
 * @params vm the vm
 */
void step(Chip8VM_t* vm);

/**
 * Fetches the next instruction then increments the program counter by 2.
 * 
 * @params  vm the vm
 * @returns    the next 
 */
word_t fetch(Chip8VM_t* vm);

/**
 * Decodes and dispatches the next opcode performing the appropraite action and
 * changing the VM state.
 * 
 * @params vm     the vm
 *         opcode the instruction opcode
 */
Instruction_t decode(word_t opcode);

/**
 * Takes the current instruction and evaluates the opcode to translate it
 * into a system call.
 * 
 * @params vm     the vm
 *         opcode the instruction opcode
 *         inst the current instruction 
 */
void evaluate(Chip8VM_t* vm, Instruction_t inst, word_t opcode);

/**
 * Performs additional changes to the VM that are not covered by instruction
 * decode and dispatch.
 * 
 * @params vm the vm
 */
void update(Chip8VM_t* vm);

/**
 * Load a ROM from a file into the vm.
 * 
 * @params vm       the vm
 *         filePath the path to the ROM
 * @returns         0 on failure
 */
int loadROM(Chip8VM_t* vm, char* filePath);

void input(Chip8VM_t*, u16);

u8 getRegisterX(word_t opcode);

u8 getRegisterY(word_t opcode);

u8 getValue8Bit(word_t opcode);

u16 getValue12Bit(word_t opcode);

u8 getValue4Bit(word_t opcode);

#endif /* CHIP8_H */
