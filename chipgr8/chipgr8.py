from chipgr8.vm      import Chip8VM
from chipgr8.vms     import Chip8VMs
from time            import sleep

import pygame
import logging

logger = logging.getLogger(__name__)

def init(
    ROM               = None,
    frequency         = 600,
    loadState         = None,
    inputHistory      = None,
    sampleRate        = 1,
    instances         = 1,
    display           = False,
    smooth            = False,
    startPaused       = False,
    aiInputMask       = 0xFFFF,
    foreground        = (255, 255, 255),
    background        = (0, 0, 0),
    theme             = None,
    unpausedDisScroll = True,
):
    '''
    Creates a new VM instance or instances with the provided configuration
    options, either returning them or allowing them to immediately enter a
    display loop. Performs some basic sanity checking on confioguration
    variables.

    @params ROM               str                   name or path to the ROM to load
            frequency         int                   frequency to run the VM at
            loadState         str                   path or tag to a save state
            inputHistory      List[int]             a list of predifined IO events
            sampleRate        int                   how many steps act moves forward
            instances         int                   the number of VMs to create
            display           bool                  if true creates a game window
            smooth            bool                  if true uses smooth rendering
            startPaused       bool                  if true starts the vm paused
            foreground        str | (int, int, int) foreground color
            background        str | (int, int, int) background color
            unpausedDisScroll bool                  if false disModule won't scroll
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
        unpausedDisScroll
    ]
    logger.info('Initializing with `{}`'.format(args))
    return Chip8VM(*args) if instances == 1 else Chip8VMs([Chip8VM(*args)
        for _
        in range(instances)
    ])