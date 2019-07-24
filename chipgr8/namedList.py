class NamedList(object):
    '''
    A list like structure that allows elements to be accessed by named 
    properties. Behaves like a python list, can be iterated, indexed, spliced, 
    and measured with len().
    '''

    names = []
    '''
    A list of keys for the list in order.
    '''

    values = []
    '''
    A list of values for the list in order.
    '''

    def __init__(self, names, values):
        self.names  = names
        self.values = values

    def __getattr__(self, name):
        return dict(zip(self.names, self.values))[name]

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, idx):
        try:
            return self.values[idx]
        except:
            return self.values[self.names.index(idx)]

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return 'NamedList({}, {})'.format(self.names, self.values)

    def append(self, name, value):
        '''
        Append a name and value to the list.
        '''
        self.names.append(name)
        self.values.append(value)

    def nparray(self):
        '''
        Retrieve the values of the list as an numpy ndarray.
        '''
        import numpy as np
        return np.array(self.values, dtype=np.dtype('uint8'))

    def tensor(self):
        '''
        Retrieve the values of the list as a tensorflow tensor.
        '''
        import tensorflow as tf
        return tf.Variable(self.values, tf.uint8)
