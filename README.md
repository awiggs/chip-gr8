[![logo](/docsource/static/img/readme-logo.png)](https://awiggs.github.io/chip-gr8/)

# Chip-Gr8 – Emulation for AI

Chip-Gr8 is a sandbox for creating AI Agents for retro video games like Pong, Breakout, and Space Invaders. Chip-Gr8 lets you interactively program AI agents, easily record their behaviour, collect data, pause and play their actions, and even play against them! If you have never programmed an AI before, Chip-Gr8 is a great place to start!

## Installing
Chip-Gr8 is a Python package. Use pip to install it!

```
pip isntall chipgr8
```

## Getting Started
If you want to play a game using Chip-Gr8, all you have to do is start it on the command line! For example, to play breakout you would run

```
python -m chipgr8 -r breakout
```

You will be greated by the Chip-Gr8 display and can start playing!

Creating an AI Agent is just as straightforward, just dropping the following code into your favorite text editor and you are ready to go!

```python
import chipgr8
from chipgr8.games import Breakout

vm = chipgr8.init(display=True, ROM=Breakout.ROM)
while not vm.done():
    vm.act(Breakout.actions.left)
```

To find out more about Chip-Gr8, its API, included games, and more examples, download the [Reference Manual](https://awiggs.github.io/chip-gr8/static/Chip-Gr8-Reference-Manual.pdf), or head over to the [docs](https://awiggs.github.io/chip-gr8/docs)!

## Contact

Feel free to contact us with questions, bug reports, or feature requests at chipgr8.contact@gmail.com.