import numpy as np
import math

class MolRepresentation:
    def __init__(self):
        self.header: {}
        self.data: np.ndarray

    def stats_calc(self): # mean and stddev calculation
        data_buffer = self.data
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

    def normalize(self):
        max_val = self.data[0]
        for i in range(len(self.data)):
            if math.fabs(self.data[i]) > max_val:
                max_val = math.fabs(self.data[i])

        self.data /= max_val