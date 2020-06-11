import numpy as np
from .denoise_method import *
from time import sleep

class MedianFilter(DenoiseMethod):
    def __init__(self, data: np.ndarray, sigma: float = 0):
        super().__init__(data)
        self.sigma = sigma

        self.window_size = 11

    def execute_3d(self):
        data = self.data
        window_size = self.window_size
        length, width, height = self.length, self.width, self.height

        edge = window_size // 2
        denoise_arr = np.zeros((length, height, width), 'f4')
        expend_data = self.__expend_array(data, edge)

        pixels_in_window = window_size * window_size * window_size

        for z in range(edge, length + edge):
            print(z / (length - window_size))
            for y in range(edge, height + edge):
                average = 0
                for j in range(window_size):
                    for i in range(window_size):
                        for k in range(window_size):
                            average += (expend_data[z + k - edge][y + j - edge][i])

                denoise_arr[z - edge][y - edge][0] = average / pixels_in_window

                for x in range(edge + 1, width + edge):
                    for j in range(window_size):
                        for k in range(window_size):
                            average += (expend_data[z + k - edge][y + j - edge][x + edge]
                                        - expend_data[z + k - edge][y + j - edge][x - edge])

                    denoise_arr[z - edge][y - edge][x - edge] = average / pixels_in_window

        return denoise_arr

    def __expend_array(self, origin_array: np.ndarray, edge:int) -> np.ndarray:
        mean_value = float(np.mean(origin_array))
        denoise_arr = np.full((self.length + 2 * edge, self.height + 2 * edge, self.width + 2 * edge), mean_value)
        denoise_arr[edge: self.length + edge, edge: self.height + edge, edge: self.width + edge] = origin_array
        return denoise_arr

    def execute_2d(self):
        data = self.data
        window_size = self.window_size
        length, width, height = self.length, self.width, self.height

        edge = window_size // 2
        denoise_arr = np.zeros((length, height, width), 'f4')
        expend_data = self.__expend_array(data, edge)

        pixels_in_window = window_size * window_size

        for z in range(edge, length + edge):
            print(z/ (length - window_size))
            for y in range(edge, height + edge):
                average = 0
                for j in range(window_size):
                    for i in range(window_size):
                        average += (expend_data[z][y + j - edge][i])

                denoise_arr[z - edge][y - edge][0] = average / pixels_in_window

                for x in range(edge + 1, width + edge):
                    for j in range(window_size):
                        average += (expend_data[z][y + j - edge][x + edge] - expend_data[z][y + j - edge][x - edge])

                    denoise_arr[z - edge][y - edge][x - edge] = average / pixels_in_window



        return denoise_arr