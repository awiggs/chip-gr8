from time import process_time

class RepeatAction(object):

    def __init__(self, delay, period, action):
        self.delay   = delay
        self.period  = period
        self.action  = action
        self.__running = False
        self.__start   = 0
        self.__last    = 0

    def start(self):
        self.__running = True
        self.__start   = process_time()
        self.__last    = self.__start

    def stop(self):
        self.__running = False
    
    def update(self):
        if not self.__running:
            return
        time = process_time()
        if time - self.__start < self.delay:
            return
        if time - self.__last >= self.period:
            self.action()
            self.__last = time