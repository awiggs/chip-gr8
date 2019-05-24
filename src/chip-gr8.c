#include <stdio.h>
#include <stdlib.h>

#include "chip8.h"

void reset(Chip8VM_t * vm);

void step(Chip8VM_t * vm);

word_t fetch(Chip8VM_t * vm);

void decode(Chip8VM_t * vm, word_t opcode);

void update(Chip8VM_t * vm);

Chip8VM_t pySteps(Chip8VM_t vm, int nSteps);

int helloWorld() {
    puts("Hello, World!");
    return EXIT_SUCCESS;
}