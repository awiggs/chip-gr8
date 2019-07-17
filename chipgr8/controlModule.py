import json
import pygame

from chipgr8.util import read, write

class ControlModule(object):

    defaultBindings = defaultKeyBindings = {
        "k0" : 120,
        "k1" : 49,
        "k2" : 50,
        "k3" : 51,
        "k4" : 113,
        "k5" : 119,
        "k6" : 101,
        "k7" : 97,
        "k8" : 115,
        "k9" : 100,
        "ka" : 122,
        "kb" : 99,
        "kc" : 52,
        "kd" : 114,
        "ke" : 102,
        "kf" : 118,
        "debugPause"    : 286,
        "debugStep"     : 287,
        "debugHome"     : 278,
        "debugEnd"      : 279,
        "debugPageUp"   : 280,
        "debugPageDown" : 281,
    }

    @staticmethod
    def validKeys():
        return list(ControlModule.defaultBindings.keys())

    def __init__(self):
        self.__bindings  = None
        self.__userInput = 0
        self.loadBindings()

    def update(self, vm, events):
        
        if vm.paused:
            for event in events:
                if event.type == pygame.QUIT:
                    vm.doneIf(True)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        vm.window.disModule.scrollUp()
                    elif event.button == 5:
                        vm.window.disModule.scrollDown()
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.__bindings["debugPause"]:
                        vm.paused = False
                    elif event.key == self.__bindings["debugStep"]:
                        vm.step()
                    elif event.key == self.__bindings["debugPageUp"]:
                        vm.window.disModule.scrollUp()
                    elif event.key == self.__bindings["debugPageDown"]:
                        vm.window.disModule.scrollDown()
                    elif event.key == self.__bindings["debugHome"]:
                        vm.window.disModule.scrollTo(0)           
                    elif event.key == self.__bindings["debugEnd"]:
                        vm.window.disModule.scrollTo(4000)
        else:
            for event in events:
                if event.type == pygame.QUIT:
                    vm.doneIf(True)
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.__bindings["debugPause"]:
                        vm.paused = True
                    elif event.key == self.__bindings["k0"]:
                        self.__userInput |= 1
                    elif event.key == self.__bindings["k1"]:
                        self.__userInput |= 1 << 1
                    elif event.key == self.__bindings["k2"]:
                        self.__userInput |= 1 << 2
                    elif event.key == self.__bindings["k3"]:
                        self.__userInput |= 1 << 3
                    elif event.key == self.__bindings["k4"]:
                        self.__userInput |= 1 << 4
                    elif event.key == self.__bindings["k5"]:
                        self.__userInput |= 1 << 5
                    elif event.key == self.__bindings["k6"]:
                        self.__userInput |= 1 << 6
                    elif event.key == self.__bindings["k7"]:
                        self.__userInput |= 1 << 7
                    elif event.key == self.__bindings["k8"]:
                        self.__userInput |= 1 << 8
                    elif event.key == self.__bindings["k9"]:
                        self.__userInput |= 1 << 9
                    elif event.key == self.__bindings["ka"]:
                        self.__userInput |= 1 << 10
                    elif event.key == self.__bindings["kb"]:
                        self.__userInput |= 1 << 11
                    elif event.key == self.__bindings["kc"]:
                        self.__userInput |= 1 << 12
                    elif event.key == self.__bindings["kd"]:
                        self.__userInput |= 1 << 13
                    elif event.key == self.__bindings["ke"]:
                        self.__userInput |= 1 << 14
                    elif event.key == self.__bindings["kf"]:
                        self.__userInput |= 1 << 15
                if event.type == pygame.KEYUP:
                    if event.key == self.__bindings["k0"]:
                        self.__userInput &= ~(1)
                    elif event.key == self.__bindings["k1"]:
                        self.__userInput &= ~(1 << 1)
                    elif event.key == self.__bindings["k2"]:
                        self.__userInput &= ~(1 << 2)
                    elif event.key == self.__bindings["k3"]:
                        self.__userInput &= ~(1 << 3)
                    elif event.key == self.__bindings["k4"]:
                        self.__userInput &= ~(1 << 4)
                    elif event.key == self.__bindings["k5"]:
                        self.__userInput &= ~(1 << 5)
                    elif event.key == self.__bindings["k6"]:
                        self.__userInput &= ~(1 << 6)
                    elif event.key == self.__bindings["k7"]:
                        self.__userInput &= ~(1 << 7)
                    elif event.key == self.__bindings["k8"]:
                        self.__userInput &= ~(1 << 8)
                    elif event.key == self.__bindings["k9"]:
                        self.__userInput &= ~(1 << 9)
                    elif event.key == self.__bindings["ka"]:
                        self.__userInput &= ~(1 << 10)
                    elif event.key == self.__bindings["kb"]:
                        self.__userInput &= ~(1 << 11)
                    elif event.key == self.__bindings["kc"]:
                        self.__userInput &= ~(1 << 12)
                    elif event.key == self.__bindings["kd"]:
                        self.__userInput &= ~(1 << 13)
                    elif event.key == self.__bindings["ke"]:
                        self.__userInput &= ~(1 << 14)
                    elif event.key == self.__bindings["kf"]:
                        self.__userInput &= ~(1 << 15)
        vm.input(self.__userInput, user=True)
        return events if vm.paused else []

    def loadBindings(self):
        try:
            self.__bindings = json.loads(read('KeyConfig.json'))
        except:
            self.__bindings = None
        self.sanityCheckBindings()

    def updateBindings(self):
        write('KeyConfig.json', json.dumps(self.__bindings, indent=4))

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
            response = input("KeyConfig.json file is corrupted.\nWould you like to restore default key bindings? (Y/n)")
            if response.lower() in ['y', 'yes']:
                self.__bindings = self.defaultBindings.copy()
                self.updateBindings()
            else:
                print("Program cannot proceed with corrupted bindings, shutting down...")
                exit(-1)

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