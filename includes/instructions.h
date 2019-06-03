#pragma once

#ifndef INST_H
#define INST_H

enum Instruction_t {
    SYS,
    ADD,
    LOAD,
    RET,
    CLEAR,
    JUMP,
    CALL,
    SKIPE,
    SKIPN,
    SKIPR,
    LOADR,
    OR,
    AND,
    XOR,
    ADDR,
    SUB,
    SUBN,
    SHIFTREG,
    SHIFTL,
    SKIPNR,
    LOADADDR,
    JUMPADDR,
    RANDOM,
    DRAW,
    SKIP,
    SKIPNP,
    LDRDT,
    LDRK,
    LDDT,
    LDST,
    ADDI,
    LDSPRI,
    LDBCD,
    LDREGS,
    LDMEM,
    NOT_IMPLEMENTED,
    INVALID_INSTRUCTION
};

typedef enum Instruction_t Instruction_t;

#endif
