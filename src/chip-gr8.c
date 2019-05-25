#include <stdio.h>
#include <stdlib.h>

#include "chip8.h"


int helloWorld() 
{
    puts("Hello, World!");
    return EXIT_SUCCESS;
}

void debug(char* message)
{
  if (DEBUG) 
  {
    puts(message);
  }
}

FILE * openRom(char* file)
{
  FILE * rom = fopen(file, "r");

  if (!rom)
  {
    debug("Failed to load rom.");
    exit(404);
  }

  return rom;
}

int loadRom(char* file)
{
  ROM = openRom(file);

  if (ROM)
  {
    return 0;
  }

  return 1;
}

int unloadRom()
{
  return closeRom(ROM);
}

u16 readInstruction()
{
  return fgetc(ROM);
}

int closeRom(FILE* rom)
{
  if (rom)
  {
    fclose(rom);
    debug("Successfully openned file");
    return 0;
  }

  debug("File not found to close");
  return 1;
}
