# The Project
The aim of this project was to design a high performance emulation engine with a Python API for integration with modern machine learning and AI libraries. Inspiration for the Chip-Gr8 project came from similar emulation + AI combinations of the NES and Atari systems.

## What is Chip-Gr8?
At its core, Chip-Gr8 is an emulator of the CHIP-8 system. Developed in the 1970's by Joseph Weisbecker, CHIP-8 was meant to be a simple system that programmers could use for beginner video game development. Many simple games, including Pong, Space Invaders, and Breakout, were programmed for the CHIP-8 throughout the 70s and 80s.

The key feature of Chip-Gr8 is the artificial intelligence (AI) API that is integrated into the emulator. This is meant to give developers an introductory experience into video game AI development, as well as modern maching learning techniques and useful AI libraries.

## Why Chip-Gr8?
As a team, we wanted a project idea that would both test our skills and that other developers would want to use. Furthermore, since none of us were particularly adept in the field of writing AI agents, we wanted to create a tool that we would have found useful had we been searching for a way to get into AI programming. With Chip-Gr8, the idea is that by providing a simplified Python API into the core of a CHIP-8 emulator, a basic programmer can pick up our tool and create their first Space Invaders, or other supported video game, AI! 

We hoped that by developing not just a marketable product, but an educational tool, that we could excite people into learning the basics of the world of artificial intelligence programming.

## Technologies Used
The Chip-Gr8 project was written in C and Python. C was used for the core CHIP-8 emulator opreations and memory management. Python was integrated closely with C using a library called CTypes. Python was used to handle the primary virtual machine structure, load/unload ROMs, as well as handling any I/O and visual display. Additional libraries used in Python were:
- NumPy
- PyGame
- Lazyarray

< More technical talk here >

# Project Timeline