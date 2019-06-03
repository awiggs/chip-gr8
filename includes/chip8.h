#pragma once

#ifndef CHIP8_H
#define CHIP8_H

#include <stdio.h>
//#include <stdlib.h>

#include "pinttypes.h"
#include "autogen_Chip8VMStruct.h"
#include "ops.h"
#include "debug.h"
#include "instructions.h"

typedef u16 word_t;

#include "autogen_Chip8VMStruct.h"

#define SHARED_LIBRARY_ID 0xAFBFCF;
/**
 * @returns a SHARED_LIBRARY_ID to ensure that the library has been loaded
 *          correctly.
 */
int helloSharedLibrary();

/**
 * Allocates a new VM instance in a valid initial sate. This is the only way a 
 * Chip-8 vm should be instantiated.
 * 
 * @returns the new VM
 */
Chip8VM_t* initVM();

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
 * Fetches the next instruction.
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
Instruction_t decode(Chip8VM_t* vm, word_t opcode);

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

u8 getRegisterX(word_t opcode);

u8 getRegisterY(word_t opcode);

u8 getValue8Bit(word_t opcode);

u8 getValue12Bit(word_t opcode);

u8 getValue4Bit(word_t opcode);

/**
 * Unlaod a ROM from a vm.
 * 
 * @params vm the vm
 * @returns   0 on failure
 */
int unloadROM(Chip8VM_t* vm);

#endif /* CHIP8_H */
