
# This is a standard configuration file for mekpie

# the name of your project
name = 'chip-gr8' 
# the .c file containing `main`
main = 'chip-gr8.c'
# the c compiler configuration to use (gcc_clang, avr_gcc, or emscripten)
cc = gcc_clang(cmd='cc', dbg='gdb')
# any libraries to load
libs = []
# additional compiler flags
flags = ['-Wall']

# Position independent code
compileflags = ['-fpic']

# Make DLL
linkflags = ['-shared']

if options.release:
    flags += ['-O']
else:
    flags += ['-g']
