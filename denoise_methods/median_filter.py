import numpy as np
from .denoise_method import *

class MedianFilter(DenoiseMethod):
    def __init__(self, data: np.ndarray, sigma: float):
        super().__init__(data)
        self.sigma = sigma

        self.window_size = 5


    def execute_3d(self):
        data = self.data
        window3d_size = self.window_size
        length, width, height = self.length, self.width, self.height
        denoise_arr: np.ndarray = data.copy()
        edge = window3d_size // 2

        for x in range(edge, width - edge):
            for y in range(edge, height - edge):
                for z in range(edge, length - edge):
                    cube_data = []
                    for i in range(window3d_size):
                        for j in range(window3d_size):
                            for k in range(window3d_size):
                                cube_data.append(data[z + k  - edge][y + j - edge][x + i - edge])

                    cube_data.sort()
                    denoise_arr[z][y][x] = cube_data[window3d_size * window3d_size * window3d_size // 2]

        return denoise_arr


    def execute_2d(self):
        data = self.data
        window_size = self.window_size
        length, width, height = self.length, self.width, self.height
        denoise_arr: np.ndarray = data.copy()
        edge = window_size // 2

        pixels_in_window = window_size * window_size

        for z in range(edge, length - edge):
            for y in range(edge, height - edge):
                average = 0
                for j in range(window_size):
                    for i in range(window_size):
                        average += (data[z][y + j - edge][i])

                denoise_arr[z][y][edge] = average / pixels_in_window

                for x in range(edge + 1, width - edge):
                    for j in range(window_size):
                        average += (data[z][y + j - edge][x - edge] - data[z][y + j - edge][x + edge])

                    denoise_arr[z][y][x] = average / pixels_in_window

        return denoise_arr