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

def disassemble(bytes=None, inPath=None, outPath=None):
    '''
    Converts a byte array or input file to a string representation of Chip-8
    instructions. Returns the result as a string and optionally writes the 
    results to a file.

    @params bytes   If provided, the instructions to decode
            inPath  If provided, the input file
            outPath If provided, the output file
    @returns        Source code
    '''
    pass #TODO