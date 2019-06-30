import os

def chunk(size, iterable, pad=[None]):
    '''
    Yields the iterable in chunks of the given size

    @params size     The size of the chunks
            iterable The iterable to chunk
    @yields          The next chunk
    '''
    for i in range(0, len(iterable), size):
        chunk = iterable[i:i + size]
        if len(chunk) < size:
                chunk += pad * (size - len(chunk))
        yield chunk

def nibbles(byte):
    '''
    @returns (high nibble, low nibble)
    '''
    return (byte >> 4, byte & 0x0F)

def hexarg(*nibbles):
    '''
    Converts any number of nibbles into a hex string 

    @params nibbles The nibbles to convert
    @returns        The hex string
    '''
    return ''.join(hex(nibble)[2:] for nibble in nibbles).upper()

def decarg(*nibles):
    '''
    Converts any number of nibbles into a decmial string

    @param nibbles The nibbles to convert
    @returns       The decimal string
    '''
    return str(int(hexarg(*nibles), 16))

def read(path, mode='r'):
    with open(path, mode) as fs:
        return fs.read()

def write(path, buffer, mode='w'):
    with open(path, mode) as fs:
        fs.write(buffer)
    return buffer

def findROM(rom):
    if not rom:
        return None
    if os.path.exists(rom):
        return rom
    rom      = rom.lower()
    romsPath = os.path.realpath(os.path.join(__file__, '../../data/roms'))
    for name in os.listdir(romsPath):
        if name.lower().startswith(rom) and name.endswith('ch8'):
            return os.path.join(romsPath, name)