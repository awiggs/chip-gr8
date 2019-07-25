import logging

from chipgr8.util import chunk, nibbles, hexarg, decarg, read, write

logger = logging.getLogger(__name__)

CHIP_8_INSTRUCTIONS = [
#   Instruction Format    Opcode
    ('CLS',               '00E0'),
    ('RET',               '00EE'),
    ('JP {nnn}',          '1nnn'),
    ('CALL {nnn}',        '2nnn'),
    ('SE V{x} {kk}',      '3xkk'),
    ('SNE V{x} {kk}',     '4xkk'),
    ('SE V{x} V{y}',      '5xy0'),
    ('LD V{x} {kk}',      '6xkk'),
    ('ADD V{x} {kk}',     '7xkk'),
    ('LD V{x} V{y}',      '8xy0'),
    ('OR V{x} V{y}',      '8xy1'),
    ('AND V{x} V{y}',     '8xy2'),
    ('XOR V{x} V{y}',     '8xy3'),
    ('ADD V{x} V{y}',     '8xy4'),
    ('SUB V{x} V{y}',     '8xy5'),
    ('SHR V{x} V{y}',     '8xy6'),
    ('SUBN V{x} V{y}',    '8xy7'),
    ('LD I {nnn}',        'Annn'),
    ('SHL V{x} V{y}',     '8xyE'),
    ('SNE V{x} V{y}',     '9xy0'),
    ('JP V0 {nnn}',       'Bnnn'),
    ('RND V{x} {kk}',     'Cxkk'),
    ('DRW V{x} V{y} {z}', 'Dxyz'),
    ('SKP V{x}',          'Ex9E'),
    ('SKNP V{x}',         'ExA1'),
    ('LD V{x} DT',        'Fx07'),
    ('LD V{x} K',         'Fx0A'),
    ('LD DT V{x}',        'Fx15'),
    ('LD ST V{x}',        'Fx18'),
    ('ADD I V{x}',        'Fx1E'),
    ('LD F V{x}',         'Fx29'),
    ('LD B V{x}',         'Fx33'),
    ('LD [I] V{x}',       'Fx55'),
    ('LD V{x} [I]',       'Fx65'),
]

RET_OP  = CHIP_8_INSTRUCTIONS[1][1]
JP_OP   = CHIP_8_INSTRUCTIONS[2][1]
CALL_OP = CHIP_8_INSTRUCTIONS[3][1]

SUPER_CHIP_48_INSTRUCTIONS = [
    ('SCU {n}',    '00nB'),
    ('SCD {n}',    '00nC'),
    ('SCR',        '00FB'),
    ('SCL',        '00FC'),
    ('EXIT',       '00FD'),
    ('LOW',        '00FE'),
    ('HIGH',       '00FF'),
    ('LD HF V{x}', 'Fx30'),
    ('LD R V{x}',  'Fx75'),
    ('LD V{x} R',  'Fx85'),
]

def hexdump(buffer=None, inPath=None, outPath=None):
    '''
    Converts a byte array or input file into a hex dump, one instruction per-line for easy diff.

    @params buffer  If provided, the instructions to dump
            inPath  if provided, the input file
            outPath If provided, the output file
    @returns        The hex dump
    '''
    if inPath: buffer = read(inPath, 'rb')
    dump = '\n'.join(hexarg(*nibbles(high), *nibbles(low))
        for (high, low) 
        in chunk(2, buffer, pad=b'\0')
    )
    if outPath: write(outPath, dump)
    return dump

def disassemble(
    buffer    = None,
    inPath    = None,
    outPath   = None,
    labels    = {},
    decargs   = True,
    srcFormat = '{label}{labelSep}{prefix}{instruction}\n',
    labelSep  = '\n',
    prefix    = '  ',
    addrTable = {},
):
    '''
    Converts a binary ROM into an assembly source file. Returns the source. 
    Provides option for disassembling with labels and special formats.

    @params buffer      The binary ROM to disassemble as a set of bytes. 
                        Optional if inPath is provided.

            inPath      The path to a binary ROM to disassemble. Optional if 
                        buffer is provided.

            outPath     If the path is provided, the source code is written to 
                        that file.

            labels      A dictionary used to generate labels. If None is passed, 
                        labels will not be generated in the source.

            decargs     If True, instruction numerical operands will be output 
                        in decimal rather than hexadecimal.

            srcFormat   A format stirng for lines of source code. Can contain 
                        the following variables label, labelSep, prefix,
                        instruction, addr, and dump. For example for hexdump 
                        with address use:

                            srcFormat='{addr} {dump}'

            labelSep    The string used to separate labels from instructions.

            prefix      The string used to prefix all instructions.                        

            addrTable   A table that will have addresses as keys and 
                        instructions as values.

    '''
    logger.info('Disassembling source: `{}` inPath: `{}` outPath: `{}`'.format(
        buffer, inPath, outPath
    ))
    buffer       = read(inPath, 'rb') if inPath else buffer
    minaddr      = 0x200
    maxaddr      = minaddr + len(buffer)
    instructions = list(chunk(1, buffer))
    remaining    = list(range(len(instructions)))
    addr         = None
    labels       = labels if isinstance(labels, dict) else None
    stack        = []

    # Disasemble all the instructions
    while addr is not None or remaining:
        addr = remaining.pop(0) if addr is None else addr
        # If next instruction is already set or invalid, skip
        if addr >= len(instructions):
            addr = None
            continue
        if type(instructions[addr]) is tuple:
            addr += 2
            continue
        # If next instuction low byte is set or invalid, set high byte to byte 
        # pseudo instruction
        if addr + 1 >= len(instructions) or type(instructions[addr + 1]) is tuple:
            high   = int.from_bytes(instructions[addr], 'big')
            hh, hl = nibbles(high)
            arg    = hexarg(hh, hl)
            instructions[addr] = ('BYTE 0x' + arg, arg, 1)
            addr = None
            continue
        # Try to proceed on the basis of a normal instruction
        (src, dump, size, nextAddr) = disassembleInstruction(
            instructions,
            stack, 
            labels, 
            decargs, 
            addr, 
            minaddr, 
            maxaddr,
        )
        for i in range(size - 1):
            instructions[addr + i + 1] = (None, None, None)
            if addr + i in remaining:
                remaining.remove(addr + i + 1)
        instructions[addr] = (src, dump, size)
        addr = nextAddr

    # Flatten instructions to source
    source = ''
    i = 0
    line = 0
    while i < len(instructions):
        src, dump, size = instructions[i]
        realAddr = minaddr + i
        i += size
        label = '{:10s}'.format(labels[realAddr]) if labels and realAddr in labels else ''
        addrTable[realAddr] = line
        source += srcFormat.format(
            label       = label, 
            instruction = src, 
            labelSep    = labelSep if label else '', 
            prefix      = prefix,
            dump        = dump, 
            addr        = realAddr,
        )
        line   += 1
    if outPath: 
        write(outPath, source)
    return source

def disassembleInstruction(instructions, stack, labels, decargs, addr, minaddr, maxaddr):
    high = int.from_bytes(instructions[addr],     'big')
    low  = int.from_bytes(instructions[addr + 1], 'big')
    (hh, hl), (lh, ll) = nibbles(high), nibbles(low)
    arguments = dict(
        x    = hexarg(hl),
        y    = hexarg(lh),
        z    = decarg(ll)     if decargs else ('0x' + hexarg(ll)),
        n    = decarg(lh)     if decargs else ('0x' + hexarg(lh)),
        kk   = decarg(lh, ll) if decargs else ('0x' + hexarg(lh, ll)),
        nnn  = '0x' + hexarg(hl, lh, ll),
    )
    # Defaults
    dump = hexarg(hh, hl, lh, ll)
    size = 2
    nextAddr = addr + 2
    for (fmt, opcode) in CHIP_8_INSTRUCTIONS:
        if opcodeMatch(opcode, dump):
            # Handle labelled addressing
            nnn = int(arguments['nnn'][2:], 16)
            if ('nnn' in fmt
                and nnn >= minaddr
                and nnn <  maxaddr
                and (opcodeMatch(JP_OP, dump) or opcodeMatch(CALL_OP, dump))
            ):
                if labels is not None and instructions[nnn - 0x200] != (None, None, None):
                    if nnn not in labels:
                        labels[nnn] = '.label_' + str(len(labels))
                    arguments['nnn'] = labels[nnn]
                # Handle RET
                if opcodeMatch(RET_OP, dump):
                    nextAddr = stack.pop() if stack else None
                # Handle JP
                if opcodeMatch(JP_OP, dump):
                    nextAddr = nnn - 0x200
                # Handle CALL
                if opcodeMatch(CALL_OP, dump):
                    stack.append(nextAddr)
                    nextAddr = nnn - 0x200
            src = fmt.format(**arguments)
            break
    else:
        src  = 'BYTE 0x' + hexarg(hh, hl)
        dump = hexarg(hh, hl)
        size = 1
        nextAddr = None
    return (src, dump, size, nextAddr)

def opcodeMatch(pattern, instruction):
    return all(p in 'xyzkn' or p == i for (p, i) in zip(pattern, instruction))