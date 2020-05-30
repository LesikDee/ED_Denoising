import math
from .denoise_method import *
import random

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class NLMeans(DenoiseMethod):
    def __init__(self, data: np.ndarray, sigma: float):
        super().__init__(data)
        self.sigma = sigma

        self.f: int = 2
        self.r: int = 10
        self.h: int = 0.4 * sigma
        self.q_arr_size = 10

    def __distance2_2d(self, p: Pixel, q: Pixel, vd_slice):
        dist_2 = 0
        f = self.f
        for j in range(-f, f + 1):
            for i in range(-f, f + 1):
                razn = vd_slice[p.y + i][p.x + j] - vd_slice[q.y + i][q.x + j]
                dist_2 += razn * razn

        return 250000.0 * dist_2 / (2 * f + 1) ** 2

    def __weight_2d(self, p: Pixel, q: Pixel, vd_slice) -> float:
        sigma, h = self.sigma * 0.1, self.h
        d_2 = self.__distance2_2d(p, q, vd_slice)
        return math.e ** -(max(d_2 - 2 * sigma * sigma, 0.0) / (h * h))


    def __precise_edges(self, p: Pixel):
        precise_p: Pixel = Pixel(p.x, p.y)

        if p.x - self.r  < 0:
            precise_p.x = self.r // 2
        if p.y - self.r  < 0:
            precise_p.y = self.r // 2

        if p.x + self.r >= self.width:
            precise_p.x = self.width - self.r  - 1
        if p.y  + self.r >= self.height:
            precise_p.y = self.height - self.r  - 1

        return precise_p


    def __generate_q_patches_arr(self, p: Pixel, arr_size) -> []:
        q_patch_arr = []
        r_range = 2 * self.r - 2 * self.f
        for q_number in range(arr_size):
            q_patch_arr.append(Pixel(p.x + random.randint(0,r_range) - r_range // 2,
                                          p.y + random.randint(0,r_range) - r_range // 2))

        return q_patch_arr

    def execute_2d(self):
        data = self.data
        length, width, height = self.length, self.width, self.height
        denoise_arr: np.ndarray = data.copy()
        for z in range(length):
            print('z', z / length)
            vd_slice = data[z]
            for y in range(height):
                #print('y', y / height)
                for x in range(width):
                    p = Pixel(x, y)
                    precise_p = self.__precise_edges(p)
                    q_arr = self.__generate_q_patches_arr(precise_p, self.q_arr_size)

                    c: float = 0
                    nl_u: float = 0
                    for q in q_arr:
                        weight = self.__weight_2d(precise_p, q, vd_slice)
                        c += weight
                        nl_u += vd_slice[p.y][p.x] * weight

                    denoise_arr[z][p.y][p.x] = nl_u / c

        return denoise_arr