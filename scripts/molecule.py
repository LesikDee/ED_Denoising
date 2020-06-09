import numpy as np

class MolRepresentation:
    def __init__(self, name: str):
        self.name = name
        self.header = None
        self.buffer: np.array #= np.array
        self.values: np.ndarray  # = np.ndarray

        self.is_normalized: bool = False

    def __stats_calc(self): # mean and stddev calculation
        self.header.mean = np.mean(self.buffer)
        self.header.stddev = np.std(self.buffer)

    def __normalize(self):
        max_val = self.buffer.max()
        min_val = self.buffer.min()

        self.buffer -= min_val
        self.buffer /= max_val - min_val


    def re_normalize(self):
        if self.is_normalized:
            return

        self.__normalize()
        self.update_from_buffer(self.buffer)
        self.__stats_calc()
        self.is_normalized = True

    def update_from_values(self, new_values: np.ndarray):
        self.values = new_values

        self.buffer = np.ravel(new_values)
        self.is_normalized = False

    def update_from_buffer(self, new_buffer: np.array):
        self.buffer = new_buffer
        header = self.header
        self.values = np.ndarray((header.fields["NS"], header.fields["NR"], header.fields["NC"]), 'f4',
                   buffer=self.buffer)

        self.is_normalized = False