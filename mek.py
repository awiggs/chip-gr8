
# This is a standard configuration file for mekpie

# the name of your project
name = 'chip-gr8' 
# the .c file containing `main`
main = 'libchip-gr8.c'
# the c compiler configuration to use (gcc_clang, avr_gcc, or emscripten)
cc = gcc_clang(cmd='gcc', dbg='gdb')
# any libraries to load
libs = []
# additional compiler flags
flags = ['-Wall', '-Werror', '-pedantic']

if options.mode == 'dll':
    linkflags = ['-shared']

if options.release:
    flags += ['-O']
else:
    flags += ['-g', '-DDEBUG']
