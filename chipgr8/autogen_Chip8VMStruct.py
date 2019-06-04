
# !!! DO NOT MODIFY THIS FILE !!!!
#
# This file was autogenerated `defineVMStruct.py`.
# If you need to modify this struct modify the definition in that file.

import ctypes

class Chip8VMStruct(ctypes.Structure):
    _pack_   = 1
    _fields_ = [
        ('RAM', ctypes.POINTER(ctypes.c_uint8)), # Main memory
        ('VRAM', ctypes.POINTER(ctypes.c_uint8)), # Video memory
        ('stack', ctypes.POINTER(ctypes.c_uint16)), # Address stack
        ('sizeRAM', ctypes.c_uint16), # Size of main memory
        ('sizeVRAM', ctypes.c_uint16), # Size of video memory
        ('sizeStack', ctypes.c_uint8), # Size of stack
        ('SP', ctypes.POINTER(ctypes.c_uint8)), # Stack pointer
        ('PC', ctypes.POINTER(ctypes.c_uint16)), # Program counter
        ('I', ctypes.POINTER(ctypes.c_uint16)), # Address register
        ('V', ctypes.POINTER(ctypes.c_uint8)), # General purpose registers
        ('DT', ctypes.POINTER(ctypes.c_uint8)), # Delay timer
        ('ST', ctypes.POINTER(ctypes.c_uint8)), # Sound timer
        ('W', ctypes.POINTER(ctypes.c_uint8)), # Wait register
        ('keys', ctypes.POINTER(ctypes.c_uint16)), # Key IO registers
        ('seed', ctypes.c_uint8), # Seed for RNG
        ('wait', ctypes.c_uint8), # Chip-8 in wait mode
        ('clock', ctypes.c_uint64), # Time since simulation began
    ]
