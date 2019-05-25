#pragma once

#ifndef CHIP8_H
#define CHIP8_H

#include <stdio.h>
#include "pinttypes.h"

#define DEBUG 1

typedef u16 word_t;

// Later these may need to be decided dynamically be Python
#define BASE       (0x200)
#define RAM_SIZE   (0xFFF)
#define VRAM_SIZE  (64 * 32)
#define STACK_SIZE (16)

FILE * ROM;

typedef struct Chip8VM_t Chip8VM_t;
struct Chip8VM_t {
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
};

int helloWorld();

void reset(Chip8VM_t * vm);

void step(Chip8VM_t * vm);

word_t fetch(Chip8VM_t * vm);

void decode(Chip8VM_t * vm, word_t opcode);

void update(Chip8VM_t * vm);

Chip8VM_t pySteps(Chip8VM_t vm, int nSteps);

void debug(char* message);

FILE * openRom(char* file);

int loadRom(char* file);

int unloadRom();

u16 readInstruction();

int closeRom(FILE* rom);
#endif /* CHIP8_H */
