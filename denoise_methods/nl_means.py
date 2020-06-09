import math
from .denoise_method import *
import random
import multiprocessing

def __distance2_2d(p: Pixel, q: Pixel, vd_slice):
    dist_2 = 0
    f = NLMeans.f
    for j in range(-f, f + 1):
        for i in range(-f, f + 1):
            razn = vd_slice[p.y + i][p.x + j] - vd_slice[q.y + i][q.x + j]
            dist_2 += razn * razn

    return 250000.0 * dist_2 / (2 * f + 1) ** 2

def __weight_2d(p: Pixel, q: Pixel, vd_slice, sigma) -> float:
    sigma, h = sigma * 0.1, 0.4 * sigma
    d_2 = __distance2_2d(p, q, vd_slice)
    return math.e ** -(max(d_2 - 2 * sigma * sigma, 0.0) / (h * h))

def __precise_edges(p: Pixel, height, width):
    precise_p: Pixel = Pixel(p.x, p.y)
    r = NLMeans.r

    if p.x - r < 0:
        precise_p.x = r // 2
    if p.y - r < 0:
        precise_p.y = r // 2

    if p.x + r >= width:
        precise_p.x = width - r - 1
    if p.y + r >= height:
        precise_p.y = height - r - 1

    return precise_p


def __generate_q_patches_arr(p: Pixel, arr_size) -> []:
    q_patch_arr = []
    r_range = 2 * NLMeans.r - 2 * NLMeans.f
    for q_number in range(arr_size):
        q_patch_arr.append(Pixel(p.x + random.randint(0, r_range) - r_range // 2,
                                 p.y + random.randint(0, r_range) - r_range // 2))

    return q_patch_arr


def multi_2d(input_tuple):
    vd_slice, height, width, sigma, z = input_tuple[0], input_tuple[1], input_tuple[2], input_tuple[3], input_tuple[4]
    denoise_arr = vd_slice.copy()
    for y in range(height):
        for x in range(width):
            p = Pixel(x, y)
            precise_p = __precise_edges(p, height, width)
            q_arr = __generate_q_patches_arr(precise_p, NLMeans.Q_ARR_SIZE)

            c: float = 0
            nl_u: float = 0
            for q in q_arr:
                weight = __weight_2d(precise_p, q, vd_slice, sigma)
                c += weight
                nl_u += vd_slice[q.y][q.x] * weight

            denoise_arr[p.y][p.x] = nl_u / c


    print(z)
    return denoise_arr

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class NLMeans(DenoiseMethod):

    Q_ARR_SIZE = 10

    r = 10

    f =  2

    def __init__(self, data: np.ndarray, sigma: float):
        super().__init__(data)
        self.sigma = sigma

        self.h: int = 0.4 * sigma


    def execute_2d(self):
        data = self.data
        length, width, height = self.length, self.width, self.height
        denoise_arr: np.ndarray = np.zeros((length, width, height), 'f4')

        # input_data = []
        # for z in range(length):
        #     input_data.append((data[z], height, width, self.sigma, z))
        #
        # p = multiprocessing.Pool(multiprocessing.cpu_count())
        # slices_map = p.map(multi_2d, input_data)
        #
        # for z in range(length):
        #     denoise_arr[z] = slices_map[z]
        z = length // 2
        data[z] = multi_2d([data[z], height, width, self.sigma, z])
        return data

