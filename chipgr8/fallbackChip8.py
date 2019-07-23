import numpy as np
import random
import hashlib

# The time to beat is 0.74
from numba import jit, njit

QRK_SHIFT = 0x01
QRK_LOAD  = 0x02

PROGRAM_START = 0x200

HEX_SPRITES = [
    0xF999F, 0x26227, 0xF1F8F, 0xF1F1F,
    0x99F11, 0xF8F1F, 0xF8F9F, 0xF1244,
    0xF9F9F, 0xF9F1F, 0xF9F99, 0xE9E9E,
    0xF888F, 0xE999E, 0xF8F8F, 0xF8F88,
]

class FallbackChip8:

    def __init__(self, freq):
        # Initialize memory and aliases
        self.RAM  = np.zeros((0x1000, ), dtype=np.uint8)
        self._defineAliases()

        # Initialize registers
        self._PC[0]  = PROGRAM_START
        self._I[0]   = PROGRAM_START
        self._FRQ[0] = freq
        self._WT[0]  = 0

        # Load hexsprites
        for i in range(0x10):
            for j in range(5):
                self.HXS[(i * 5) + j] = ((HEX_SPRITES[i] >> ((4 - j) * 4) & 0xF) << 4)
    
    def __defineAlias(self, size, dtype):
        save = self.base
        self.base += size
        return self.RAM[save : save + size].view(dtype=dtype)

    def __storeHexsprite(self, i, sprite):
        for j in range(5):
            self.HXS[(i * 5) + j] = ((sprite >> ((4 - j) * 4) & 0xF) << 4)

    def _defineAliases(self):

        u8  = np.uint8
        u16 = np.uint16
        u64 = np.uint64

        self.base = 0x000
        self.HXS  = self.__defineAlias(0x50,  u8 )
        self.VRAM = self.__defineAlias(0x100, u8 )
        self.STK  = self.__defineAlias(0x20,  u16)
        self.V    = self.__defineAlias(0x10,  u8 )
        self._SP  = self.__defineAlias(0x1,   u8 )
        self._PC  = self.__defineAlias(0x2,   u16)
        self._I   = self.__defineAlias(0x2,   u16)
        self._DT  = self.__defineAlias(0x1,   u8 )
        self._ST  = self.__defineAlias(0x1,   u8 )
        self._W   = self.__defineAlias(0x1,   u8 )
        self._WT  = self.__defineAlias(0x1,   u8 )
        self._K   = self.__defineAlias(0x2,   u16)
        self._CLK = self.__defineAlias(0x8,   u64)
        self._FRQ = self.__defineAlias(0x1,   u8 )
        self._QRK = self.__defineAlias(0x1,   u8 )
        # TODO remove and replace with hook
        self._DIFF_X = self.__defineAlias(0x1, u8)
        self._DIFF_Y = self.__defineAlias(0x1, u8)
        self._DIFF_SIZE = self.__defineAlias(0x1, u8)
        self._DIFF_CLEAR = self.__defineAlias(0x1, u8)

    def _sha1(self):
        return hashlib.sha1(self.RAM.view(np.uint8)).hexdigest()

    @property
    def SP(self):
        return self._SP[0]

    @property
    def PC(self):
        return self._PC[0]

    @property
    def I(self):
        return self._I[0]

    @property
    def DT(self):
        return self._DT[0]

    @property
    def ST(self):
        return self._ST[0]

    @property
    def W(self):
        return self._W[0]

    @property
    def WT(self):
        return self._WT[0]

    @property
    def K(self):
        return self._K[0]

    @property
    def CLK(self):
        return self._CLK[0]

    @property
    def quirks(self):
        return self._QRK[0]

    @property
    def clock(self):
        return self._CLK[0]

    @property
    def diffX(self):
        return self._DIFF_X[0]

    @property
    def diffY(self):
        return self._DIFF_Y[0]

    @property
    def diffClear(self):
        return self._DIFF_CLEAR[0]

    @property
    def diffSize(self):
        return self._DIFF_SIZE[0]

    @property
    def diffSkip(self):
        return 0

    @quirks.setter
    def quirks(self, quirks):
        self._QRK[0] = quirks

    def input(self, k):
        self._K[0] = k
        if k and self._WT[0]:
            decodedK = 0
            # Decode keys, get most significant bit key
            while k >> 1:
                k >>= 1
                decodedK += 1
            # Assign to wait register V[W]
            self.V[self._W[0]] = decodedK
            # Stop waiting
            self._WT[0] = 0

    def step(self):
        step(   
            self.RAM,
            self.VRAM,
            self.STK,
            self.V,
            self._SP,
            self._PC,
            self._I,
            self._DT,
            self._ST,
            self._W,
            self._WT,
            self._K,
            self._CLK,
            self._FRQ,
            self._QRK,
            self._DIFF_X,
            self._DIFF_Y,
            self._DIFF_SIZE,
            self._DIFF_CLEAR,
        )

    def loadROM(self, ROM):
        data = np.fromfile(ROM, dtype=np.uint8)
        self.RAM[PROGRAM_START : PROGRAM_START + len(data)] = data
        return True

@njit
def step(
    RAM,
    VRAM,
    STK,
    V,
    SP,
    PC,
    I,
    DT,
    ST,
    W,
    WT,
    K,
    CLK,
    FRQ,
    QRK,
    DIFF_X,
    DIFF_Y,
    DIFF_SIZE,
    DIFF_CLEAR,
):
    preStep(RAM, CLK, DIFF_SIZE, DIFF_CLEAR)
    if not WT[0]:
        opcode, l, x, y, kk, nnn, n = decode(fetch(RAM, PC))
        if l == 0x0:
            if opcode == 0x00E0:
                opCLS(VRAM, DIFF_CLEAR)
            elif opcode == 0x00EE:
                opRET(STK, SP, PC)
        elif l == 0x1:
            opJP(PC, nnn)
        elif l == 0x2:
            opCALL(STK, SP, PC, nnn)
        elif l == 0x3:
            opSEValue(V, PC, x, kk)
        elif l == 0x4:
            opSNEValue(V, PC, x, kk)
        elif l == 0x5:
            opSEReg(V, PC, x, y)
        elif l == 0x06:
            opLDValue(V, x, kk)
        elif l == 0x07:
            opADDValue(V, x, kk)
        elif l == 0x08:
            if n == 0x0:
                opLDReg(V, x, y)
            elif n == 0x1:
                opOR(V, x, y)
            elif n == 0x2:
                opAND(V, x, y)
            elif n == 0x3:
                opXOR(V, x, y)
            elif n == 0x4:
                opADDReg(V, x, y)
            elif n == 0x5:
                opSUB(V, x, y)
            elif n == 0x6:
                opSHR(V, QRK, x, y)
            elif n == 0x7:
                opSUBN(V, x, y)
            elif n == 0xE:
                opSHL(V, QRK, x, y)
        elif l == 0x9:
            opSNEReg(V, PC, x, y)
        elif l == 0xA:
            opLDI(I, nnn)
        elif l == 0xB:
            opJPV0(V, PC, nnn)
        elif l == 0xC:
            opRND(V, CLK, x, kk)
        elif l == 0xD:
            opDRW(RAM, VRAM, V, I, DIFF_X, DIFF_Y, DIFF_SIZE, x, y, n)
        elif l == 0xE:
            if n == 0xE:
                opSKP(V, PC, K, x)
            else:
                opSKNP(V, PC, K, x)
        elif l == 0xF:
            if kk == 0x07:
                opLDRegDT(V, DT, x)
            elif kk == 0x0A:
                opLDRegKey(WT, W, x)
            elif kk == 0x15:
                opLDDT(V, DT, x)
            elif kk == 0x18:
                opLDST(V, ST, x)
            elif kk == 0x1E:
                opADDI(V, I, x)
            elif kk == 0x29:
                opLDSprite(V, I, x)
            elif kk == 0x33:
                opLDBCD(RAM, V, I, x)
            elif kk == 0x55:
                opLDRegs(RAM, V, I, QRK, x)
            elif kk == 0x65:
                opLDMem(RAM, V, I, QRK, x)
    postStep(DT, ST, CLK, FRQ)

@njit
def preStep(RAM, CLK, DIFF_SIZE, DIFF_CLEAR):
    # Reset diff flags
    DIFF_SIZE[0]  = 0
    DIFF_CLEAR[0] = 0
    # Increment the clock
    CLK[0] += 1

@njit
def postStep(DT, ST, CLK, FRQ):
    # Update timers at 60Hz
    if CLK[0] % FRQ[0] == 0:
        # Decrement DT and ST if positive
        if DT[0] > 0: DT[0] -= 1 
        if ST[0] > 0: ST[0] -= 1

@njit
def fetch(RAM, PC):
    msb = (0 + RAM[PC[0]]) << 8 # Add zero to force conversion to python int
    lsb = (0 + RAM[PC[0] + 1])  # Add zero to force conversion to python int
    PC[0] += 2
    return msb + lsb

@njit
def decode(opcode):
    l   = (opcode & 0xF000) >> 12
    x   = (opcode & 0x0F00) >> 8
    y   = (opcode & 0x00F0) >> 4
    kk  =  opcode & 0x00FF
    nnn =  opcode & 0x0FFF
    n   =  opcode & 0x000F
    return (opcode, l, x, y, kk, nnn, n)

@njit
def opCLS(VRAM, DIFF_CLEAR):
    '''
    Instruction: 00E0
    Description: Clear the display.
    @params VRAM   The display buffer
    '''
    DIFF_CLEAR[0] = 1
    VRAM.fill(0)

@njit
def opRET(STK, SP, PC):
    '''
    Instruction: 00EE
    Description: Return from a subroutine.
    @params STK The address stack
            SP  The stack pointer
            PC  The program counter
    '''
    SP[0] -= 1
    PC[0]  = STK[SP[0]]

@njit
def opJP(PC, nnn):
    '''
    Instruction: 1nnn
    Description: Jump to location nnn.
    @params PC  The program counter
            nnn the address
    '''
    PC[0] = nnn

@njit
def opCALL(STK, SP, PC, nnn):
    '''
    Instruction: 2nnn
    Description: Call subroutine at nnn.
    @params STK The address stack
            SP  The stack pointer
            PC  The program counter
            nnn The address
    '''
    STK[SP[0]] = PC[0]
    SP[0]     += 1
    PC[0]      = nnn

@njit
def opSEValue(V, PC, x, kk):
    '''
    Instruction: 3xkk
    Description: Skip next instruction if the value of register Vx equals kk.
    @params V   The general purpose registers
            PC  The program counter
            x   The Vx index
            kk  The value
    '''
    if V[x] == kk:
        PC[0] += 2

@njit
def opSNEValue(V, PC, x, kk):
    '''
    Instruction: 4xkk
    Description: Skip next instruction if the value of register Vx does not equal kk.
    @params V   The general purpose registers
            PC  The program counter
            x   The Vx index
            kk  The value
    '''
    if V[x] != kk:
        PC[0] += 2

@njit
def opSEReg(V, PC, x, y):
    '''
    Instruction: 5xy0
    Description: Skip next instruction if the value of register Vx equals the value
                 of register Vy.
    @params V   The general purpose registers
            PC  The program counter
            x   The Vx index
            y   The Vy index
    '''
    if V[x] == V[y]:
        PC[0] += 2 

@njit
def opLDValue(V, x, kk):
    '''
    Instruction: 6xkk
    Description: Set the value of register Vx to kk.
    @params V   The general purpose registers
            x   The Vx index
            kk  The value
    '''
    V[x] = kk

@njit
def opADDValue(V, x, kk):
    '''
    Instruction: 7xkk
    Description: Set the value of register Vx to the value of register Vx plus kk.
    @params V   The general purpose registers
            x   The Vx index
            kk  The value
    '''
    V[x] += kk

@njit
def opLDReg(V, x, y):
    '''
    Instruction: 8xy0
    Description: Set the value of register Vx to the value of register Vy.
    @params V   The general purpose registers
            x   The Vx index
            y   The Vy index
    '''
    V[x] = V[y]

@njit
def opOR(V, x, y):
    '''
    Instruction: 8xy1
    Description: Set the value of register Vx to the bitwise OR of the values of
                 registers Vx and Vy.
    @params V   The general purpose registers
            x   The Vx index
            y   The Vy index
    '''
    V[x] |= V[y]

@njit
def opAND(V, x, y):
    '''
    Instruction: 8xy2
    Description: Set the value of register Vx to the bitwise AND of the values of
                 registers Vx and Vy.
    @params V   The gneral purpose registers
            x   The Vx index
            y   The Vy index
    '''
    V[x] &= V[y]

@njit
def opXOR(V, x, y):
    '''
    Instruction: 8xy3
    Description: Set the value of register Vx to the bitwise exclusive OR of the
                 values of registers Vx and Vy.
    @params V   The general purpose registers
            x   The Vx index
            y   The Vy index
    '''
    V[x] ^= V[y]

@njit
def opADDReg(V, x, y):
    '''
    Instruction: 8xy4
    Description: Set the value of register Vx to the value of register Vx plus the
                 value of register Vy and set the carry flag VF.
    @params V   The general purpose registers
            x   The Vx index
            y   The By index
    '''
    a = V[x]
    b = V[y]
    c = (0 + a) + b # We add zero to force conversion to python int
    V[0xF] = (c >> 8) & 0x1
    V[x]   = c & 0xFF

@njit
def opSUB(V, x, y):
    '''
    Instruction: 8xy5
    Description: Set the value of register Vx to the value of register Vx minus the
                 value of register Vy and set the borrow flag VF.
    @params V   The general purpose registers
            x   The Vx index
            y   The Vy index
    '''
    a = V[x]
    b = V[y]
    c = (0 + a) - b # We add zero to force conversion to python int
    V[0xF] = a >= b
    V[x]   = c & 0xFF

@njit
def opSHR(V, QRK, x, y):
    '''
    Instruction: 8xy6
    Description: Default behaviour is to shift the value of register Vx to the right,
                 store the result in Vx, and set the flag VF accordingly. When a ROM
                 has the SHIFT_QUIRK flag set, the behaviour is to shift the value of
                 register Vy to the right, store the result in Vx, and set the flag
                 VF accordingly.
    @params V   The general purpose registers
            QRK The quirks registers
            x   The Vx index
            y   The Vy index
    '''
    if not (QRK[0] & QRK_SHIFT):
        y = x
    V[0xF] = V[y] & 0x1
    V[x]   = V[y] >> 1

@njit
def opSUBN(V, x, y):
    '''
    Instruction: 8xy7
    Description: Set the value of register Vx to the value of register Vy minus the
                value of register Vx and set the borrow flag VF.
    @params V   The general purpose registers
            x   The Vx index
            y   The Vy index
    '''
    a = V[y]
    b = V[x]
    c = (0 + a) - b # We add zero to force conversion to python int
    V[0xF] = a >= b
    V[x]   = c & 0xFF

@njit
def opSHL(V, QRK, x, y):
    '''
    Instruction: 8xyE
    Description: Default behaviour is to shift the value of register Vx to the left,
                store the result in Vx, and set the flag VF accordingly. When a ROM
                has the SHIFT_QUIRK flag set, the behaviour is to shift the value of
                register Vy to the left, store the result in Vx, and set the flag
                VF accordingly.
    @params V   The general purpose registers
            QRK The quirks register
            x   The Vx index
            y   The Vy index
    '''
    if not (QRK[0] & QRK_SHIFT):
        y = x
    V[0xF] = V[y] & 0x8
    V[x]   = V[y] << 1

@njit
def opSNEReg(V, PC, x, y):
    '''
    Instruction: 9xy0
    Description: Skip next instruction if the value of register Vx does not equal the
                value of register Vy.
    @params V   The general purpose registers
            PC  The program counter
            x   The Vx index
            y   The Vy index
    '''
    if V[x] != V[y]:
        PC[0] += 2

@njit
def opLDI(I, nnn):
    '''
    Instruction: Annn
    Description: Set the value of register I to the address nnn.
    @params I   The address register
            nnn The address
    '''
    I[0] = nnn

@njit
def opJPV0(V, PC, nnn):
    '''
    Instruction: Bnnn
    Description: Jump to location nnn plus the value of register V0.
    @params V   The general purpose registers
            PC  The program counter
            nnn The address
    '''
    PC[0] = nnn + V[0x0]

@njit
def opRND(V, CLK, x, kk):
    '''
    Instruction: Cxkk
    Description: Set the value of register Vx to the bitwise AND of kk and a random
                 number between 0 and 255.
    @params V   The general purpose registers
            x   The Vx index
            kk  The value
    '''
    random.seed(CLK[0])
    V[x] = random.randint(0, 255) & kk

@njit
def opDRW(RAM, VRAM, V, I, DIFF_X, DIFF_Y, DIFF_SIZE, x, y, n):
    '''
    Instruction: Dxyn
    Description: Display an n-byte sprite starting at memory location I at coordinates
                 (Vx, Vy) and set the collision flag VF.
    @params RAM     Main memory
            VRAM    The display bufffer
            V       The general purpose registers
            I       The address registers
            x       The Vx index
            y       The Vy index
            n       The size of the sprite in bytes
    '''
    i = I[0]
    x = V[x]
    y = V[y]
    DIFF_X[0] = x
    DIFF_Y[0] = y
    DIFF_SIZE[0] = n
    V[0xF] = 0
    
    # for each row of the sprite
    for j in range(n):
        
        # get the sprite data byte
        spriteByte = RAM[i + j]

        # calculate the intended coordinates
        row = (y + j) % 32
        col = x % 64
        
        # calculate corresponding location in VRAM
        bit          = ((row * 64) + col)
        firstByte    = bit // 8
        secondByte   = (row * 8) if col >= 56 else (firstByte + 1)
        bitOffset    = bit % 8
        leftoverBits = 8 - bitOffset
        
        # get the existing VRAM data for the intended location
        oldVRAMData = (
            (VRAM[firstByte]  << bitOffset) | 
            (VRAM[secondByte] >> leftoverBits)
        )

        # compare to set the collision flag
        if oldVRAMData & spriteByte:
            V[0xF] = 1
        
        # set VRAM memory
        VRAM[firstByte]  ^= (spriteByte >> bitOffset)
        VRAM[secondByte] ^= (spriteByte << leftoverBits)

@njit
def opSKP(V, PC, K, x):
    '''
    Instruction: Ex9E
    Description: Skip next instruction if key with the value in register Vx is pressed.
    @params V   The general purpose registers
            PC  The program counter
            K   The keys register
            x   The Vx index
    '''
    if (K[0] >> V[x]) & 1:
        PC[0] += 2

@njit
def opSKNP(V, PC, K, x):
    '''
    Instruction: ExA1
    Description: Skip next instruction if key with the value in register Vx is not
                 pressed.
    @params V   The general purpose registers
            PC  The program counter
            K   The keys register
            x   The Vx index
    '''
    if not ((K[0] >> V[x]) & 1):
        PC[0] += 2

@njit
def opLDRegDT(V, DT, x):
    '''
    Instruction: Fx07
    Description: Set the value of register Vx to the delay timer value.
    @params V   The general purpose registers
            DT  The delay timer register
            x   The Vx index
    '''
    V[x] = DT[0]

@njit
def opLDRegKey(WT, W, x):
    '''
    Instruction: Fx0A
    Description: Wait for a key press, store the number of register Vx into the wait register.
    @params WT  The wait register
            W   The wait V store register
            x   The Vx index
    '''
    WT[0] = 1
    W[0]  = x

@njit
def opLDDT(V, DT, x):
    '''
    Instruction: Fx15
    Description: Set the delay timer to the value of register Vx.
    @params V   The general purpose registers
            DT  The delay timer register
            x   The Vx index
    '''
    DT[0] = V[x]

@njit
def opLDST(V, ST, x):
    '''
    Instruction: Fx18
    Description: Set the sound timer to the value of register Vx.
    @params V   The general purpose registers
            ST  The sound timer register
            x   The Vx index
    '''
    ST[0] = V[x]

@njit
def opADDI(V, I, x):
    '''
    Instruction: Fx1E
    Description: Set the value of register I to the value of register I plus the value
                of register Vx.
                of register Vx.
    @params V   The general purpose registers
            I   The address register
            x   The Vx index
    '''
    I[0] += V[x]

@njit
def opLDSprite(V, I, x):
    '''
    Instruction: Fx29
    Description: Set the value of register I to the location of the sprite corresponding
                to the value of register Vx. Each hex sprite is five bytes long.
                to the value of register Vx. Each hex sprite is five bytes long.
    @params V   The general purpose registers
            I   The address register
            x   The Vx index
    '''
    I[0] = V[x] * 5

@njit
def opLDBCD(RAM, V, I, x):
    '''
    Instruction: Fx33
    Description: Store the Binary Coded Decimal representation of Vx in memory locations
                 I, I+1, and I+2.
    @params RAM Main Memory
            V   The general purpose registers
            I   The address register
            x   The Vx index
    '''
    i = I[0]
    a = V[x]
    RAM[i + 0] = (a // 100) % 10
    RAM[i + 1] = (a // 10 ) % 10
    RAM[i + 2] = (a // 1  ) % 10

@njit
def opLDRegs(RAM, V, I, QRK, x):
    '''
    Instruction: Fx55
    Description: Store the value of memory starting at location I into registers V0
                 through Vx. Default behaviour is to leave the value of I unaffected.
                 When a ROM has the LOAD_QUIRK flag set, the behaviour is to increment
                 the value of I.
    @params RAM Main memory
            V   The general purpose registers
            I   The address register
            QRK The quirk register
            x   The Vx register
    '''
    i = I[0]
    for j in range(x + 1):
        RAM[i + j] = V[j]
    if QRK[0] & QRK_LOAD:
        I[0] += x + 1

@njit
def opLDMem(RAM, V, I, QRK, x):
    '''
    Instruction: Fx65
    Description: Store the value of memory starting at location I into registers V0
                 through Vx. Default behaviour is to leave the value of I unaffected.
                 When a ROM has the LOAD_QUIRK flag set, the behaviour is to increment
                 the value of I.
    @params RAM Main memory
            V   The general purpose registers
            I   The address registers
            QRK The quirks register
            x   The Vx index
    '''
    i = I[0]
    for j in range(x + 1):
        V[j] = RAM[i + j]
    if QRK[0] & QRK_LOAD:
        I[0] += x + 1