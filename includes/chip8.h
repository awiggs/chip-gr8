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

#if defined(_WIN32) || defined(_WIN64)
    #define shared __declspec( dllexport )
#else
    #define shared
#endif

#define PROGRAM_SPACE_START 0x200

#define HEXSPRITE_0         0xF999F
#define HEXSPRITE_1         0x26227
#define HEXSPRITE_2         0xF1F8F
#define HEXSPRITE_3         0xF1F1F
#define HEXSPRITE_4         0x99F11
#define HEXSPRITE_5         0xF8F1F
#define HEXSPRITE_6         0xF8F9F
#define HEXSPRITE_7         0xF1244
#define HEXSPRITE_8         0xF9F9F
#define HEXSPRITE_9         0xF9F1F
#define HEXSPRITE_A         0xF9F99
#define HEXSPRITE_B         0xE9E9E
#define HEXSPRITE_C         0xF888F
#define HEXSPRITE_D         0xE999E
#define HEXSPRITE_E         0xF8F8F
#define HEXSPRITE_F         0xF8F88

// To avoid defining very large int literals, interlaces hexsprite int literal with 0s
// such that 0x11111 becomes 0x1010101010 then stores each byte to arr
#define STORE_HEXSPRITE(_arr, _ind, _spr)   SAFE_MACRO( \
                                                u32 _hex = _spr; \
                                                for(u8 _i = 0; _i < 5; _i++){ \
                                                    *(_arr + (_ind * 5) + _i) = ((_hex >> ((4 - _i) * 4) & 0xF) << 4); \
                                                } \
                                            )

#define SHIFT_QUIRK 0x01
#define LOAD_QUIRK  0x02
#define DRAW_QUIRK  0x04

/* Needed for building with cl and distutils */
void PyInit_libchip_gr8();

typedef u16 word_t;

#include "autogen_Chip8VMStruct.h"

#define SHARED_LIBRARY_ID 0xAFBFCF;
/**
 * @returns a SHARED_LIBRARY_ID to ensure that the library has been loaded
 *          correctly.
 */
shared int helloSharedLibrary();

/**
 * Initializes a VM instance to a valid initial sate. This is the only way a 
 * Chip-8 vm should be instantiated.
 * 
 * @params vm   the vm to intialize
 *         freq the frequency as a factor of 60Hz
 */
shared void initVM(Chip8VM_t* vm, u8 freq);

/**
 * Steps a VM 1 clock cycle. 
 * 
 * @params vm the vm
 */
shared void step(Chip8VM_t* vm);

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
 * Load a ROM from a file into the vm.
 * 
 * @params vm       the vm
 *         filePath the path to the ROM
 * @returns         0 on failure
 */
shared int loadROM(Chip8VM_t* vm, char* filePath);

shared void input(Chip8VM_t*, u16);

u8 getRegisterX(word_t opcode);

u8 getRegisterY(word_t opcode);

u8 getValue8Bit(word_t opcode);

u16 getValue12Bit(word_t opcode);

u8 getValue4Bit(word_t opcode);

#endif /* CHIP8_H */
