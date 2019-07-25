from chipgr8.vm      import Chip8VM
from chipgr8.vms     import Chip8VMs
from time            import sleep

import pygame
import logging

logger = logging.getLogger(__name__)

def init(
    ROM          = None,
    frequency    = 600,
    loadState    = None,
    inputHistory = None,
    sampleRate   = 1,
    instances    = 1,
    display      = False,
    smooth       = False,
    startPaused  = False,
    aiInputMask  = 0xFFFF,
    foreground   = (255, 255, 255),
    background   = (0, 0, 0),
    theme        = None,
    autoScroll   = True,
    speed        = 1,
):
    '''
    Returns an instance of Chip8VM or Chip8VMs. Used to configure the virtual 
    machines for a user or a given AI agent.

    @params ROM             If provided will load a ROM into the vm instance or 
                            instances.

            frequency       The starting frequency of the vm instance or 
                            instances. Will automatically be set to the closest
                            multiple of 60 less than or equal to the provided 
                            frequency.

            loadState       A path or tag to a vm save state that will be 
                            loaded into each vm instance or instances.

            inputHistory    If provided user and AI input will be ignored and 
                            the history will be used to reproduce the same 
                            events.

            sampleRate      The number of steps that are performed when an AI 
                            calls act.

            instances       The number of vm instances to create.

            display         If True, the vm will create a CHIP-GR8 display. 
                            Cannot be True if instances does not equal 1.

            smooth          If True, enables the experimental smooth rendering 
                            mode. This mode is slow on most machines.

            startPaused     If True, the vm instance will start paused.

            aiInputMask     The keys usable to the AI agent as a bitmask. The 
                            keys available to the user are the bitwise inverse 
                            of this mask.

            foregound       The foreground color of the CHIP-GR8 display as an 
                            RGB tuple or hex code.

            background      The background color of the CHIP-GR8 display as an 
                            RGB tuple or hex code.

            theme           The foreground/background color provided as a tuple.
            
            autoScoll       If True, this disassembly source will automatically 
                            scroll when the CHIP-GR8 display is open and a ROM 
                            is running.

            speed           The speed at which the UI is tied to the Chip-8
                            frequency. So when speed is 1, games will appear to
                            run at the provided freq, but when speed is 2, games
                            will appear to run twice as fast.
    '''
    # Some simple sanity checks
    assert instances > 0,                 'Must have some number of instances!'
    assert instances == 1 or not display, 'Cannot create multiple display instances!'
    assert not smooth or display,         '`smooth` is a display specific setting!'
    assert not startPaused or display,    '`startPaused` is a display specific setting!'

    if theme:
        foreground, background = theme

    args = [
        ROM, 
        frequency, 
        loadState, 
        inputHistory,
        sampleRate,
        display,
        smooth,
        startPaused,
        aiInputMask,
        pygame.Color(foreground) if type(foreground) == str else foreground,
        pygame.Color(background) if type(background) == str else background,
        autoScroll,
        speed,
    ]
    logger.info('Initializing with `{}`'.format(args))
    return Chip8VM(*args) if instances == 1 else Chip8VMs([Chip8VM(*args)
        for _
        in range(instances)
    ])