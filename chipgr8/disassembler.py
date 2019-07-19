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
    logger.info('Hexdumping buffer: `{}` inPath: `{}` outPath: `{}`'.format(
        buffer, inPath, outPath
    ))
    if inPath: buffer = read(inPath, 'rb')

    dump = '\n'.join(hexarg(*nibbles(high), *nibbles(low))
        for (high, low) 
        in chunk(2, buffer, pad=b'\0')
    )
    if outPath: write(outPath, dump)
    return dump

def disassemble(
    buffer   = None, 
    inPath   = None, 
    outPath  = None, 
    labels   = {}, 
    decargs  = True, 
    prefix   = '  ', 
    hexdump  = False,
    labelSep = '\n  ',
):
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
            hexdump Show hex value of line as a comment
    @returns        Disassembled source code
    '''
    logger.info('Disassembling source: `{}` inPath: `{}` outPath: `{}`'.format(
        buffer, inPath, outPath
    ))
    if inPath: 
        buffer = read(inPath, 'rb')
    if not isinstance(labels, dict): 
        labels = None
    minaddr = 0x200
    maxaddr = minaddr + len(buffer)
    instructions = [disassembleInstruction(high, low, labels, decargs, minaddr, maxaddr, hexdump)
        for (high, low)
        in chunk(2, buffer, pad=b'\0')
    ]
    source = ''
    for (i, instruction) in enumerate(instructions):
        addr = '0x' + hexarg(minaddr + (i * 2))
        if labels and addr in labels:
            source += '{:10s}{}'.format(labels[addr], labelSep)
        else:
            source += prefix
        source += instruction.replace('\n', '\n' + prefix) + '\n'

    if outPath: write(outPath, source)
    return source

def disassembleInstruction(high, low, labels, decargs, minaddr, maxaddr, hexdump):
    (hh, hl), (lh, ll) = nibbles(high), nibbles(low)
    arguments = dict(
        x    = hexarg(hl),
        y    = hexarg(lh),
        z    = decarg(ll)     if decargs else ('0x' + hexarg(ll)),
        n    = decarg(lh)     if decargs else ('0x' + hexarg(lh)),
        kk   = decarg(lh, ll) if decargs else ('0x' + hexarg(lh, ll)),
        nnn  = '0x' + hexarg(hl, lh, ll),
    )
    for (fmt, opcode) in CHIP_8_INSTRUCTIONS:
        if opcodeMatch(opcode, hexarg(hh, hl, lh, ll)):
            # Handle labelled addressing
            nnn = int(arguments['nnn'][2:], 16)
            if (labels is not None 
                and 'nnn' in fmt 
                and nnn >= minaddr
                and nnn <  maxaddr
                and nnn %  2 == 0
            ):
                if arguments['nnn'] not in labels:
                    labels[arguments['nnn']] = '.label_' + str(len(labels))
                arguments['nnn'] = labels[arguments['nnn']]
            return fmt.format(**arguments) + (' ; 0x' + hexarg(hh, hl, lh, ll) if hexdump else '')

    for (fmt, opcode) in SUPER_CHIP_48_INSTRUCTIONS:
        if opcodeMatch(opcode, hexarg(hh, hl, lh, ll)):
            return fmt.format(**arguments)
    
    return 'BYTE 0x' + hexarg(hh, hl) + '\nBYTE 0x' + hexarg(lh, ll)

def opcodeMatch(pattern, instruction):
    return all(p in 'xyzkn' or p == i for (p, i) in zip(pattern, instruction))