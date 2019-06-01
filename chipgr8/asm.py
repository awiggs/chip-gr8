from chipgr8.util import chunk, nibbles, hexarg, decarg, read, write

def assemble(src=None, inPath=None, outPath=None):
    '''
    Converts a string representation or input file of Chip-8 instructions to a 
    binary ROM and optionally writes the results to a file. Returns result as a 
    bytearray. Consider assembly syntax defined here: 
    https://massung.github.io/CHIP-8/

    @params src     If provided, the string source code
            inPath  If provided, the input file
            outPath If provided, the output file
    @returns        ROM binary
    '''
    pass #TODO

CHIP_8_INSTRUCTIONS = [
#   Instruction Format    Opcode
    ('CLS',               '00E0'),
    ('RET',               '00EE'),
    ('JP {addr}',         '1nnn'),
    ('CALL {addr}',       '2nnn'),
    ('SE V{x} {kk}',      '3xkk'),
    ('SNE V{x} {kk}',     '4xkk'),
    ('SE V{x} V{y}',      '5xy0'),
    ('LD V{x} {kk}',      '6xkk'),
    ('ADD V{x} {kk}',     '7xkk'),
    ('Ld V{x} V{y}',      '8xy0'),
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
    ('JP V0 {nnn}',       'Annn'),
    ('RND V{x} {kk}',     'Cxkk'),
    ('DRW V{x} V{y} {n}', 'Dxyn'),
    ('SKP V{x}',          'Ex9E'),
    ('SKNO V{x}',         'ExA1'),
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

def disassemble(buffer=None, inPath=None, outPath=None, labels={}, decargs=True, prefix='  '):
    '''
    Converts a byte array or input file to a string representation of Chip-8
    instructions. Returns the result as a string and optionally writes the 
    results to a file.

    @params buffer  If provided, the instructions to decode
            inPath  If provided, the input file
            outPath If provided, the output file
            labels  If a dictionary generate labels for CALL and JP instructions
            decargs If True express non address values in decimal
            prefix  Prefix prior to instruction, defaults to two spaces
    @returns        Disassembled source code
    '''
    # Get buffer from provided path if needed
    if inPath: buffer = read(inPath, 'rb')

    instructions = [disassembleInstruction(high, low, labels, decargs)
        for (high, low) 
        in chunk(2, buffer)
    ]
    source = ''
    for (i, instruction) in enumerate(instructions):
        addr = '0x' + hexarg(0x200 + (i * 2))
        if labels and addr in labels:
            source += labels[addr] + '\n'
        source += prefix + instruction + '\n'

    if outPath: write(outPath, source)
    return source

def disassembleInstruction(high, low, labels, decargs):
    (hh, hl), (lh, ll) = nibbles(high), nibbles(low)
    parameters = dict(
        x    = hexarg(hl),
        y    = hexarg(lh),
        n    = decarg(ll)     if decargs else ('0x' + hexarg(ll)),
        kk   = decarg(lh, ll) if decargs else ('0x' + hexarg(lh, ll)),
        nnn  = '0x' + hexarg(hl, lh, ll),
        addr = '0x' + hexarg(hl, lh, ll),
    )
    for (fmt, opcode) in CHIP_8_INSTRUCTIONS:
        if opcodeMatch(opcode, hexarg(hh, hl, lh, ll)):
            # Handle labelled addressing
            if labels is not None and 'addr' in fmt:
                if parameters['nnn'] not in labels:
                    labels[parameters['nnn']] = '.label_' + str(len(labels))
                parameters['addr'] = labels[parameters['nnn']]
            return fmt.format(**parameters)

    for (fmt, opcode) in SUPER_CHIP_48_INSTRUCTIONS:
        if opcodeMatch(opcode, hexarg(high, low)):
            return fmt.format(**parameters)
    
    return 'BYTE 0x' + hexarg(high, low)

def opcodeMatch(pattern, instruction):
    return all(p in 'xykn' or p == i for (p, i) in zip(pattern, instruction))