#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "chip8.h"

/**
 * @returns a SHARED_LIBRARY_ID to ensure that the library has been loaded
 *          correctly.
 */
int helloSharedLibrary() {
    return SHARED_LIBRARY_ID;
}

/**
 * Allocates a new VM instance in a valid initial sate. This is the only way a 
 * Chip-8 vm should be instantiated.
 * 
 * @returns the new VM
 */
Chip8VM_t* initVM() {
    // #TODO initialize VM state correctly.
    Chip8VM_t* vm = malloc(sizeof(Chip8VM_t));
    vm->ROM = NULL;
    return vm;
}

/**
 * Deallocates a VM instance. The VM instance should NOT be accessed after
 * being passed to this function.
 * 
 * @params vm the vm to deallocate
 */
void freeVM(Chip8VM_t* vm) {
    // #TODO perform any other necessary cleanup (eg. closing ROM file)
    if (vm->ROM != NULL) {
        unloadROM(vm);
    }
    free(vm);
}

/**
 * Steps a VM 1 clock cycle. 
 * 
 * @params vm the vm
 */
void step(Chip8VM_t* vm) {
    // #TODO
}

/**
 * Fetches the next instruction.
 * 
 * @params  vm the vm
 * @returns    the next 
 */
word_t fetch(Chip8VM_t* vm) {
    // #TODO
    return fgetc(vm->ROM);    
}

/**
 * Decodes and dispatches the next opcode performing the appropraite action and
 * changing the VM state.
 * 
 * @params vm     the vm
 *         opcode the instruction opcode
 */
void decode(Chip8VM_t* vm, word_t opcode) {
    // #TODO
}

/**
 * Performs additional changes to the VM that are not covered by instruction
 * decode and dispatch.
 * 
 * @params vm the vm
 */
void update(Chip8VM_t* vm) {
    // #TODO
}

/**
 * Load a ROM from a file into the vm.
 * 
 * @params vm       the vm
 *         filePath the path to the ROM
 * @returns         0 on failure
 */
int loadROM(Chip8VM_t* vm, char* filePath) {
    vm->ROM = fopen(filePath, "r");
    if (vm->ROM == NULL) {
        debugf("Failed to load rom: %s", filePath);
    }
    debugs("Succesfully opened ROM file.");
    return vm->ROM != NULL;
}

/**
 * Unlaod a ROM from a vm.
 * 
 * @params vm the vm
 * @returns   0 on failure
 */
int unloadROM(Chip8VM_t* vm) {
    if (vm->ROM) {
        fclose(vm->ROM);
        debugs("Succesfully closed ROM file.");
        return 0;
    }
    debugs("No ROM file to close!");
    return 1;
}
