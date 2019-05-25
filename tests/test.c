#include <stdio.h>
#include "chip8.h"

int main(int argv, char* argc)
{
  int success = loadRom("./data/roms/Tron.ch8");
  if (success)
  {
    printf("The first instruction is %i.", readInstruction());
    unloadRom();
  }
  else
  {
    puts("Failed to load rom.");
  }

  return success;
}
