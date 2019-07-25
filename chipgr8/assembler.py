import re
import logging 

from chipgr8.util import read, write

logger = logging.getLogger(__name__)

V_REGISTERS = [
    'V0', 'V1', 'V2', 'V3',
    'V4', 'V5', 'V6', 'V7',
    'V8', 'V9', 'VA', 'VB',
    'VC', 'VD', 'VE', 'VF',
]

def assemble(source=None, inPath=None, outPath=None):
    '''
    Converts assembly source code, or source code contained in inPath into 
    binary data (a ROM). This ROM may optionally be written to file with the 
    outPath argument.

    @params source  If provided, the string source code
            inPath  If provided, the input file
            outPath If provided, the output file
    @returns        ROM binary
    '''
    logger.info('Assembling source: `{}` inPath: `{}` outPath: `{}`'.format(
        source, inPath, outPath
    ))
    if inPath: source = read(inPath)

    (lines, labels) = retrieveLabels(source)
    buffer = b''
    for line in lines:
        buffer += assembleLine(line, labels)

    if outPath: write(outPath, buffer, 'wb')
    return buffer

def retrieveLabels(source):
    offset = 0x200
    labels = {}
    lines  = []
    for (i, line) in enumerate(source.split('\n')):
        line = line.strip()
        line = re.sub(r';.*', '', line)
        # Blank
        if len(line) == 0:
            continue
        # Comment
        if line.startswith(';'):
            continue
        # Constant
        if line.startswith('$'):
            (name, value, *rest) = line.split()
            labels[name] = value
        # Label
        if line.startswith('.'):
            labels[line] = str(offset)
        # Instruction
        else:
            lines.append((line, i + 1))
            offset += 1 if line.lower().startswith('byte') else 2
    return (lines, labels)

def assembleLine(line, labels):
    (source, lineno)     = line
    (instruction, *rest) = source.split()
    instruction          = instruction.upper()
    if instruction not in ASSEMBLY_TABLE:
        raise Exception('Unknown instruction {} on line {}!'.format(instruction, lineno))
    try:
        return bytes.fromhex(ASSEMBLY_TABLE[instruction](rest, labels, lineno))
    except Exception as error:
        raise Exception(str(error) + '\n    at "' + source + '"')

def assembleValue(source, labels, lineno, nibbles):
    # constant
    if source.startswith('$'):
        if source not in labels:
            raise Exception('Unknown constant {} on line {}!'.format(source, lineno))
        return assembleValue(labels[source], labels, lineno, nibbles)
    # label
    if source.startswith('.'):
        if source not in labels:
            raise Exception('Unknown label {} on line {}!'.format(source, lineno))
        return assembleValue(labels[source], labels, lineno, nibbles)
    # hex
    if re.match(r'0x[\daAbBcCdDeEfF]+$', source):
        source = source[2:]
        if len(source) > nibbles:
            raise Exception('Invalid size value {} on line {}!'.format(source, lineno))
        padding = nibbles - len(source)
        return '0' * padding + source
    # bin
    if re.match(r'0b[01]+$', source):
        hexSource = hex(int(source[2:], 2))[2:]
        if len(hexSource) > nibbles:
            raise Exception('Invalid size value {} on line {}!'.format(source, lineno))
        padding = nibbles - len(hexSource)
        return '0' * padding + hexSource
    # decimal
    if re.match(r'\d+$', source):
        hexSource = hex(int(source))[2:]
        if len(hexSource) > nibbles:
            raise Exception('Invalid size value {} on line {}!'.format(source, lineno))
        padding = nibbles - len(hexSource)
        return '0' * padding + hexSource
    raise Exception('Unknown value {} on line {}!'.format(source, lineno))

def isRegister(source, labels):
    # check if in registers
    if source.upper() in V_REGISTERS:
        return True
    # constant
    if source.startswith('$'):
        return source in labels and isRegister(labels[source], labels)
    return False

def assembleRegister(source, labels, lineno):
    # check if in registers
    if source.upper() in V_REGISTERS:
        return source[1].upper()
    # constant
    if source.startswith('$'):
        if source not in labels:
            raise Exception('Unknown constant {} on line {}!'.format(source, lineno))
        return assembleRegister(labels[source], source, lineno)
    raise Exception('Expected a register {} on line {}!'.format(source, lineno))

def assembleCommand(hex):
    def assembleCommandImpl(arguments, labels, lineno):
        if len(arguments) == 0:
            return hex
        raise Exception('Unexpected number of arguments on line {}!'.format(lineno))
    return assembleCommandImpl 

def assembleVRegOp(prefix, postfix):
    def assembleVRegOpImpl(arguments, labels, lineno):
        if len(arguments) == 2:
            Vx = assembleRegister(arguments[0], labels, lineno)
            Vy = assembleRegister(arguments[1], labels, lineno)
            return prefix + Vx + Vy + postfix
        raise Exception('Unexpected number of arguments on line {}!'.format(lineno))
    return assembleVRegOpImpl

def assembleJP(arguments, labels, lineno):
    if len(arguments) == 1:
        nnn = assembleValue(arguments[0], labels, lineno, 3)
        return '1' + nnn
    if len(arguments) == 2:
        V0  = arguments[0].upper()
        nnn = assembleValue(arguments[1], labels, lineno, 3)
        if V0 != 'V0':
            raise Exception('Unexpected arguments {} on line {}!'.format(V0, lineno))
        return 'B' + nnn
    raise Exception('Unexpected number of arguments on line {}!'.format(lineno))

def assembleCALL(arguments, labels, lineno):
    if len(arguments) == 1:
        nnn = assembleValue(arguments[0], labels, lineno, 3)
        return '2' + nnn
    raise Exception('Unexpected number of arguments on line {}!'.format(lineno))
    
def assembleSE(arguments, labels, lineno):
    if len(arguments) == 2:
        Vx = assembleRegister(arguments[0], labels, lineno)
        if isRegister(arguments[1], labels):
            Vy = assembleRegister(arguments[1], labels, lineno)
            return '5' + Vx + Vy + '0'
        else:
            kk = assembleValue(arguments[1], labels, lineno, 2)
            return '3' + Vx + kk
    raise Exception('Unexpected number of arguments on line {}!'.format(lineno))

def assembleSNE(arguments, labels, lineno):
    if len(arguments) == 2:
        Vx = assembleRegister(arguments[0], labels, lineno)
        if isRegister(arguments[1], labels):
            Vy = assembleRegister(arguments[1], labels, lineno)
            return '9' + Vx + Vy + '0'
        else:
            kk = assembleValue(arguments[1], labels, lineno, 2)
            return '4' + Vx + kk
    raise Exception('Unexpected number of arguments on line {}!'.format(lineno))

def assembleLD(arguments, labels, lineno):
    if len(arguments) == 2:
        if isRegister(arguments[0], labels):
            Vx = assembleRegister(arguments[0], labels, lineno)
            if isRegister(arguments[1], labels):
                Vy = assembleRegister(arguments[1], labels, lineno)
                return '8' + Vx + Vy + '0'
            elif arguments[1].upper() == 'DT':
                return 'F' + Vx + '07'
            elif arguments[1].upper() == 'K':
                return 'F' + Vx + '0A'
            elif arguments[1].upper() == '[I]':
                return 'F' + Vx + '65'
            elif arguments[1].upper() == 'R':
                return 'F' + Vx + '85'
            else:
                kk = assembleValue(arguments[1], labels, lineno, 2)
                return '6' + Vx + kk
        if isRegister(arguments[1], labels):
            Vx = assembleRegister(arguments[1], labels, lineno)
            if arguments[0].upper() == 'DT':
                return 'F' + Vx + '15'
            if arguments[0].upper() == 'ST':
                return 'F' + Vx + '18'
            if arguments[0].upper() == 'F':
                return 'F' + Vx + '29'
            if arguments[0].upper() == 'B':
                return 'F' + Vx + '33' 
            if arguments[0].upper() == '[I]':
                return 'F' + Vx + '55'
            if arguments[0].upper() == 'HF':
                return 'F' + Vx + '30'
            if arguments[0].upper() == 'R':
                return 'F' + Vx + '75'
        if arguments[0].upper() == 'I':
            nnn = assembleValue(arguments[1], labels, lineno, 3)
            return 'A' + nnn
    raise Exception('Unexpected arguments on line {}!'.format(lineno))

def assembleADD(arguments, labels, lineno):
    if len(arguments) == 2:
        if isRegister(arguments[0], labels):
            Vx = assembleRegister(arguments[0], labels, lineno)
            if isRegister(arguments[1], labels):
                Vy = assembleRegister(arguments[1], labels, lineno)
                return '8' + Vx + Vy + '4'
            else:
                kk = assembleValue(arguments[1], labels, lineno, 2)
                return '7' + Vx + kk
        if isRegister(arguments[1], labels):
            Vx = assembleRegister(arguments[1], labels, lineno)
            if arguments[0].upper() == 'I':
                return 'F' + Vx + '1E'
    raise Exception('Unexpected arguments on line {}!'.format(lineno))

def assembleRND(arguments, labels, lineno):
    if len(arguments) == 2:
        Vx = assembleRegister(arguments[0], labels, lineno)
        kk = assembleValue(arguments[1], labels, lineno, 2)
        return 'C' + Vx + kk
    raise Exception('Unexpected number of arguments on line {}!'.format(lineno))

def assembleDRW(arguments, labels, lineno):
    if len(arguments) == 3:
        Vx = assembleRegister(arguments[0], labels, lineno)
        Vy = assembleRegister(arguments[1], labels, lineno)
        n  = assembleValue(arguments[2], labels, lineno, 1)
        return 'D' + Vx + Vy + n
    raise Exception('Unexpected number of arguments on line {}!'.format(lineno))

def assembleSKP(arguments, labels, lineno):
    if len(arguments) == 1:
        Vx = assembleRegister(arguments[0], labels, lineno)
        return 'E' + Vx + '9E'
    raise Exception('Unexpected number of arguments on line {}!'.format(lineno))

def assembleSKNP(arguments, labels, lineno):
    if len(arguments) == 1:
        Vx = assembleRegister(arguments[0], labels, lineno)
        return 'E' + Vx + 'A1'
    raise Exception('Unexpected number of arguments on line {}!'.format(lineno))

def assembleSCU(arguments, labels, lineno):
    if len(arguments) == 1:
        n = assembleValue(arguments[0], labels, lineno, 1)
        return '00' + n + 'B'
    raise Exception('Unexpected number of arguments on line {}!'.format(lineno))

def assembleSCD(arguments, labels, lineno):
    if len(arguments) == 1:
        n = assembleValue(arguments[0], labels, lineno, 1)
        return '00' + n + 'C'
    raise Exception('Unexpected number of arguments on line {}!'.format(lineno))

def assembleBYTE(arguments, labels, lineno):
    if len(arguments) == 1:
        bb = assembleValue(arguments[0], labels, lineno, 2)
        return bb
    raise Exception('Unexpected number of arguments on line {}!'.format(lineno))

ASSEMBLY_TABLE = {
    'CLS':  assembleCommand('00E0'),
    'RET':  assembleCommand('00EE'),
    'JP':   assembleJP,
    'CALL': assembleCALL,
    'SE':   assembleSE,
    'SNE':  assembleSNE,
    'LD':   assembleLD,
    'ADD':  assembleADD,
    'OR':   assembleVRegOp('8', '1'),
    'AND':  assembleVRegOp('8', '2'),
    'XOR':  assembleVRegOp('8', '3'),
    'SUB':  assembleVRegOp('8', '5'),
    'SHR':  assembleVRegOp('8', '6'),
    'SUBN': assembleVRegOp('8', '7'),
    'SHL':  assembleVRegOp('8', 'E'),
    'RND':  assembleRND,
    'DRW':  assembleDRW,
    'SKP':  assembleSKP,
    'SKNP': assembleSKNP,
    'SCU':  assembleSCU,
    'SCD':  assembleSCD,
    'SCR':  assembleCommand('00FB'),
    'SCL':  assembleCommand('00FC'),
    'EXIT': assembleCommand('00FD'),
    'LOW':  assembleCommand('00FE'),
    'HIGH': assembleCommand('00FF'),
    'BYTE': assembleBYTE,
}