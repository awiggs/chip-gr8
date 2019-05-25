#include <stdio.h>
#include "chip8.h"

int main(int argv, char** argc)
{
  int success = loadRom("./data/roms/Tron.ch8");
  if (success)
  {
    for (int i = 0; i < 10; i++)
    {
      printf("The %ith instruction is %02x.\n", i, readInstruction());
    }

    unloadRom();
  }
  else
  {
    puts("Failed to load rom.");
  }

  return 0;
}
