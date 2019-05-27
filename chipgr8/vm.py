class Chip8VM(object):

    VRAM = None
    RAM  = None

    def __init__(self):
        pass #TODO

    def io(self, handler, raw=None):
        raise Exception('Implement Me!')

    def step(self):
        raise Exception('Implement Me!')

    def steps(self, n):
        raise Exception('Implement Me!')

    def loop(self):
        raise Exception('Implement Me!')

    def getBitMap(self):
        '''
        Description: Converts the ctypes info to a nice python bitmap and returns that value
        @return     [32][64]    A 2d list of size 32x64 with:
                                The first level represents each row of the screen's pixels
                                The second level represents each column of that row
                                Each value is either 0 or 1
                                    0 -> black pixel
                                    1 -> white pixel
        '''
        pass #TODO