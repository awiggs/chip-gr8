#pragma once

#ifndef CHIP8_H
#define CHIP8_H

#include "pinttypes.h"
#include "debug.h"

typedef u16 word_t;

#define SHARED_LIBRARY_ID 0xAFBFCF;

// Later these may need to be decided dynamically be Python
#define BASE       (0x200)
#define RAM_SIZE   (0xFFF)
#define VRAM_SIZE  (64 * 32)
#define STACK_SIZE (16)

typedef struct Chip8VM_t Chip8VM_t;
struct Chip8VM_t 
{
    // Add Fields as needed!
    u8 RAM[RAM_SIZE];
    u8 VRAM[VRAM_SIZE];
    u16 stack[STACK_SIZE];
    u8 SP;    // stack pointer
    u16 PC;   // program counter
    u16 I;    // address pointer 
    u8 V[16]; // general purpose registers
    u8 DT;    // Delay timer register
    u8 ST;    // Sound timer register
    u8 keys[16];
    u64 clock;
    u64 cycles;
    FILE * ROM;
};

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
void decode(Chip8VM_t* vm, word_t opcode);

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

/**
 * Unlaod a ROM from a vm.
 * 
 * @params vm the vm
 * @returns   0 on failure
 */
int unloadROM(Chip8VM_t* vm);

#endif /* CHIP8_H */
