#include <stdio.h>
#include "chip8.h"

int main()
{
  int success = loadRom("./data/roms/Tron.ch8");
  if (success)
  {
    unloadRom();
  }

  return success;
}
