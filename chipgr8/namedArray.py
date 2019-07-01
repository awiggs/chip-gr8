class NamedArray(object):

    names    = None
    values   = None

    def __init__(self, names, values):
        self.names  = names
        self.values = values

    def __getattr__(self, name):
        return dict(zip(self.names, self.values))[name]

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, idx):
        return self.values[idx]

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return 'NamedArray({}, {})'.format(self.names, self.values)

    def nparray(self):
        import numpy as np
        return np.array(self.values, dtype=np.dtype('uint8'))

    def tensor(self):
        import tensorflow as tf
        return tf.Variable(self.values, tf.uint8)
