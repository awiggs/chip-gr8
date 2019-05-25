#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

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

  if (rom == NULL)
  {
    debug("Failed to load rom.");
    exit(404);
  }

  return rom;
}

int loadRom(char* file)
{
  ROM = openRom(file);

  if (ROM != NULL)
  {
    return true;
  }

  return false;
}

int unloadRom()
{
  return closeRom(ROM);
}

wint_t readInstruction()
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
