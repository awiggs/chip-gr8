import json
import pygame
import logging

logger = logging.getLogger(__name__)

from chipgr8.util         import read, write
from chipgr8.repeatAction import RepeatAction

class ControlModule(object):

    ctrlHeld = False

    defaultBindings = {
        'k0' : pygame.K_x,
        'k1' : pygame.K_1,
        'k2' : pygame.K_2,
        'k3' : pygame.K_3,
        'k4' : pygame.K_q,
        'k5' : pygame.K_w,
        'k6' : pygame.K_e,
        'k7' : pygame.K_a,
        'k8' : pygame.K_s,
        'k9' : pygame.K_d,
        'ka' : pygame.K_z,
        'kb' : pygame.K_c,
        'kc' : pygame.K_4,
        'kd' : pygame.K_r,
        'ke' : pygame.K_f,
        'kf' : pygame.K_v,
        'reset' : pygame.K_F7, 
        'quit'  : pygame.K_ESCAPE,  
        'debugPause'    : pygame.K_F5,
        'debugStep'     : pygame.K_F6,
        'debugHome'     : pygame.K_HOME,
        'debugEnd'      : pygame.K_END,
        'debugPageUp'   : pygame.K_PAGEUP,
        'debugPageDown' : pygame.K_PAGEDOWN,
    }

    @staticmethod
    def validKeys():
        return list(ControlModule.defaultBindings.keys())

    def __init__(self):
        self.__bindings   = None
        self.__userInput  = 0
        self.__stepper    = None
        self.__mouseClock = pygame.time.Clock()
        self.loadBindings()

    def update(self, vm, events):
        # Initialize and update the stepper
        if not self.__stepper:
            self.__stepper = RepeatAction(0.5, 0.1, lambda : vm.step())
        else:
            self.__stepper.update()
        # Handle the events
        for event in events:
            if event.type == pygame.QUIT:
                logger.info('Quit event')
                if vm.done():
                    error = Exception('Trying to quit a done vm! Are you sure you are in a while not done loop?')
                    logger.error(exc_info=error)
                    raise error
                vm.doneIf(True)
            if event.type == pygame.KEYDOWN:
                if event.key == self.__bindings['reset']:
                    logger.debug('Key pressed: `reset`')
                    vm.reset()
                elif event.key == self.__bindings['quit']:
                    logger.debug('Key pressed `quit`')
                    vm.doneIf(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    self.ctrlHeld = True
                    vm._window.disModule.showUnderlines(self.ctrlHeld)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.ctrlHeld = False
                    vm._window.disModule.showUnderlines(self.ctrlHeld)
            if event.type == pygame.MOUSEBUTTONDOWN and not vm.autoScroll:
                if event.button == 1:
                    self.__mouseClock.tick()
                    if self.__mouseClock.get_time() < 300:
                        logger.debug('Mouse double-clicked')
                        if not self.ctrlHeld:
                            addr = vm._window.disModule.getClickedAddr(event.pos)
                            if addr > -1:
                                msg = vm.toggleBreakpoint(addr)
                                logger.debug(msg)
                    else:
                        logger.debug('Mouse left-clicked')
                        if self.ctrlHeld:
                            logger.debug('Mouse ctrl-clicked')
                            vm._window.disModule.jumpToMousedLabel()
                elif event.button == 4:
                    logger.debug('Scroll moved up')
                    vm._window.disModule.scrollUp()
                elif event.button == 5:
                    logger.debug('Scroll moved down')
                    vm._window.disModule.scrollDown()

            if event.type == pygame.MOUSEMOTION:
                vm._window.disModule.updateMouseOverLine(event.pos)
        if vm.paused:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.__mouseClock.tick()
                        if self.__mouseClock.get_time() < 300:
                            logger.debug('Mouse double-clicked')
                            if not self.ctrlHeld:
                                addr = vm._window.disModule.getClickedAddr(event.pos)
                                if addr > -1:
                                    msg = vm.toggleBreakpoint(addr)
                                    logger.debug(msg)
                        else:
                            logger.debug('Mouse left-clicked')
                            if self.ctrlHeld:
                                logger.debug('Mouse ctrl-clicked')
                                vm._window.disModule.jumpToMousedLabel()
                    elif event.button == 4:
                        logger.debug('Scroll moved up')
                        vm._window.disModule.scrollUp()
                    elif event.button == 5:
                        logger.debug('Scroll moved down')
                        vm._window.disModule.scrollDown()
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.__bindings['debugPause']:
                        logger.debug('Key pressed: `debugPause`')
                        vm.paused = False
                    elif event.key == self.__bindings['debugStep']:
                        logger.debug('Key pressed: `debugStep`')
                        self.__stepper.start()
                        vm.step()
                    elif event.key == self.__bindings['debugPageUp']:
                        logger.debug('Key pressed: `debugPageUp`')
                        vm._window.disModule.scrollUp()
                    elif event.key == self.__bindings['debugPageDown']:
                        logger.debug('Key pressed: `debugPageDown`')
                        vm._window.disModule.scrollDown()
                    elif event.key == self.__bindings['debugHome']:
                        logger.debug('Key pressed: `debugHome`')
                        vm._window.disModule.scrollTo(0)
                    elif event.key == self.__bindings['debugEnd']:
                        logger.debug('Key pressed: `End`')
                        vm._window.disModule.scrollTo(4000)
                elif event.type == pygame.KEYUP:
                    if event.key == self.__bindings['debugStep']:
                        self.__stepper.stop()
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == self.__bindings['debugPause']:
                        logger.debug('Key pressed: `debugPause`')
                        vm.paused = True
                    elif event.key == self.__bindings['k0']:
                        logger.debug('Key pressed: `k0`')
                        self.__userInput |= 1
                    elif event.key == self.__bindings['k1']:
                        logger.debug('Key pressed: `k1`')
                        self.__userInput |= 1 << 1
                    elif event.key == self.__bindings['k2']:
                        logger.debug('Key pressed: `k2`')
                        self.__userInput |= 1 << 2
                    elif event.key == self.__bindings['k3']:
                        logger.debug('Key pressed: `k3`')
                        self.__userInput |= 1 << 3
                    elif event.key == self.__bindings['k4']:
                        logger.debug('Key pressed: `k4`')
                        self.__userInput |= 1 << 4
                    elif event.key == self.__bindings['k5']:
                        logger.debug('Key pressed: `k5`')
                        self.__userInput |= 1 << 5
                    elif event.key == self.__bindings['k6']:
                        logger.debug('Key pressed: `k6`')
                        self.__userInput |= 1 << 6
                    elif event.key == self.__bindings['k7']:
                        logger.debug('Key pressed: `k7`')
                        self.__userInput |= 1 << 7
                    elif event.key == self.__bindings['k8']:
                        logger.debug('Key pressed: `k8`')
                        self.__userInput |= 1 << 8
                    elif event.key == self.__bindings['k9']:
                        logger.debug('Key pressed: `k9`')
                        self.__userInput |= 1 << 9
                    elif event.key == self.__bindings['ka']:
                        logger.debug('Key pressed: `ka`')
                        self.__userInput |= 1 << 10
                    elif event.key == self.__bindings['kb']:
                        logger.debug('Key pressed: `kb`')
                        self.__userInput |= 1 << 11
                    elif event.key == self.__bindings['kc']:
                        logger.debug('Key pressed: `kc`')
                        self.__userInput |= 1 << 12
                    elif event.key == self.__bindings['kd']:
                        logger.debug('Key pressed: `kd`')
                        self.__userInput |= 1 << 13
                    elif event.key == self.__bindings['ke']:
                        logger.debug('Key pressed: `ke`')
                        self.__userInput |= 1 << 14
                    elif event.key == self.__bindings['kf']:
                        logger.debug('Key pressed: `kf`')
                        self.__userInput |= 1 << 15
                if event.type == pygame.KEYUP:
                    if event.key == self.__bindings['k0']:
                        logger.debug('Key released: `k0`')
                        self.__userInput &= ~(1)
                    elif event.key == self.__bindings['k1']:
                        logger.debug('Key released: `k1`')
                        self.__userInput &= ~(1 << 1)
                    elif event.key == self.__bindings['k2']:
                        logger.debug('Key released: `k2`')
                        self.__userInput &= ~(1 << 2)
                    elif event.key == self.__bindings['k3']:
                        logger.debug('Key released: `k3`')
                        self.__userInput &= ~(1 << 3)
                    elif event.key == self.__bindings['k4']:
                        logger.debug('Key released: `k4`')
                        self.__userInput &= ~(1 << 4)
                    elif event.key == self.__bindings['k5']:
                        logger.debug('Key released: `k5`')
                        self.__userInput &= ~(1 << 5)
                    elif event.key == self.__bindings['k6']:
                        logger.debug('Key released: `k6`')
                        self.__userInput &= ~(1 << 6)
                    elif event.key == self.__bindings['k7']:
                        logger.debug('Key released: `k7`')
                        self.__userInput &= ~(1 << 7)
                    elif event.key == self.__bindings['k8']:
                        logger.debug('Key released: `k8`')
                        self.__userInput &= ~(1 << 8)
                    elif event.key == self.__bindings['k9']:
                        logger.debug('Key released: `k9`')
                        self.__userInput &= ~(1 << 9)
                    elif event.key == self.__bindings['ka']:
                        logger.debug('Key released: `ka`')
                        self.__userInput &= ~(1 << 10)
                    elif event.key == self.__bindings['kb']:
                        logger.debug('Key released: `kb`')
                        self.__userInput &= ~(1 << 11)
                    elif event.key == self.__bindings['kc']:
                        logger.debug('Key released: `kc`')
                        self.__userInput &= ~(1 << 12)
                    elif event.key == self.__bindings['kd']:
                        logger.debug('Key released: `kd`')
                        self.__userInput &= ~(1 << 13)
                    elif event.key == self.__bindings['ke']:
                        logger.debug('Key released: `ke`')
                        self.__userInput &= ~(1 << 14)
                    elif event.key == self.__bindings['kf']:
                        logger.debug('Key released: `kf`')
                        self.__userInput &= ~(1 << 15)
        vm.input(self.__userInput, user=True)
        return events if vm.paused else []

    def loadBindings(self):
        try:
            self.__bindings = json.loads(read('chipgr8.keys.json'))
        except:
            logger.warning('No `KeyConfig.json`, using default bindings')
            self.__bindings = self.defaultBindings.copy()
        self.sanityCheckBindings()

    def updateBindings(self):
        write('chipgr8.keys.json', json.dumps(self.__bindings, indent=4))

    def sanityCheckBindings(self):

        validKeyConfig = True
        bindingsUsed   = []
        validKeys      = ControlModule.validKeys()

        if self.__bindings is None:
            validKeyConfig = False
        else:
            for (key, binding) in self.__bindings.items():
                if binding not in bindingsUsed and type(binding) == int:
                    bindingsUsed.append(binding)
                else:
                    validKeyConfig = False
                    break
                try:
                    validKeys.remove(key)
                except:
                    validKeyConfig = False
                    break
            if not len(validKeys) == 0:
                validKeyConfig = False

        if not validKeyConfig:
            response = input('chipgr8.keys.json was invalid.\nWould you like to restore default key bindings? (Y/n)')
            if response.lower() in ['y', 'yes']:
                self.__bindings = self.defaultBindings.copy()
                self.updateBindings()
            else:
                raise Exception('Inbalid Binding: `KeyConfig.json` was invalid')

    def setKeyBinding(self, newBindings):

        invalidValues = list(self.__bindings.values())
        validKeys     = ControlModule.validKeys()

        for key in newBindings:
            if key in self.__bindings:
                invalidValues.remove(self.__bindings[key])    

        for (key, binding) in newBindings.items():
            if key not in validKeys:
                raise Exception('Invalid Binding: `{}` is not a valid key! Use `print(ControlModule.validKeys())` to see all valid keys.'.format(key))
            if not type(binding) == int:
                raise Exception('Invalid Binding: `{}` is not an integer keycode!'.format(binding))
            if binding in invalidValues:
                raise Exception('Invalid Binding: `{}` is already in use!'.format(binding))
            self.__bindings[key] = binding

        self.updateBindings()