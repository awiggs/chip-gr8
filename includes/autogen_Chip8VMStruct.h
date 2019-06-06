
#pragma once

/**
 * !!! DO NOT MODIFY THIS FILE !!!
 *
 * This file was autogenerated `defineVMStruct.py`.
 * If you need to modify this struct modify the definition in that file.
 */

#ifndef AUTOGEN_VMSTRUCT_H
#define AUTOGEN_VMSTRUCT_H

/* !!! DO NOT MODIFY !!! */
typedef struct Chip8VM_t Chip8VM_t;
struct Chip8VM_t {
    u8* RAM; // Main memory
    u8* VRAM; // Video memory
    u16* stack; // Address stack
    u16 sizeRAM; // Size of main memory
    u16 sizeVRAM; // Size of video memory
    u8 sizeStack; // Size of stack
    u8* SP; // Stack pointer
    u16* PC; // Program counter
    u16* I; // Address register
    u8* V; // General purpose registers
    u8* DT; // Delay timer
    u8* ST; // Sound timer
    u8* W; // Wait register
    u16* keys; // Key IO registers
    u8 seed; // Seed for RNG
    u8 wait; // Chip-8 in wait mode
    u64 clock; // Time since simulation began
    u8* hexes; // Hexsprite pointer
} __attribute__((packed));

#endif /* AUTOGEN_VMSTRUCT_H */
