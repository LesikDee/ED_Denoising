import numpy as np

class MolRepresentation:
    def __init__(self):
        self.header: {}
        self.buffer: np.array #= np.array
        self.values: np.ndarray  # = np.ndarray

        self.is_normalized: bool = False

    def __stats_calc(self): # mean and stddev calculation
        data_buffer = self.buffer
        n = len(data_buffer)
        mean = 0
        for i in range(n):
            mean += data_buffer[i]

        mean /= n
        self.header.mean = mean

        stddev = 0
        for i in range(n):
            stddev += (data_buffer[i] - mean) ** 2

        stddev = (stddev / n) ** 0.5
        self.header.stddev = stddev

    def __normalize(self):
        max_val = self.buffer.max()
        min_val = self.buffer.min()

        self.buffer -= min_val
        self.buffer /= max_val - min_val

    def re_normalize(self):
        if self.is_normalized:
            return

        self.__normalize()
        self.__stats_calc()
        self.is_normalized = True

    def update_values(self, new_values: np.ndarray):
        self.values = new_values

        self.buffer = np.ravel(new_values)
        self.is_normalized = False
