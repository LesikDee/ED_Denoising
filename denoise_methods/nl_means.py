import math
from .denoise_method import *
import random
import multiprocessing

def __distance2_2d(p: Pixel, q: Pixel, vd_slice):
    f = NLMeans.f
    dist_m = vd_slice[p.y - f: p.y + f + 1, p.x - f: p.x + f + 1] - \
             vd_slice[q.y - f: q.y + f + 1 , q.x - f: q.x + f + 1]

    dist_2 = np.sum(dist_m ** 2)
    return dist_2 / (2 * f + 1) ** 2

def weight_2d(p: Pixel, q: Pixel, vd_slice, sigma) -> float:
    sigma2 = 0.0007
    h2 = 1.4 * sigma2
    d_2 = __distance2_2d(p, q, vd_slice)
    #print(d_2, math.e ** -(max(d_2 - sigma2, 0.0) / h2))
    return math.e ** -(max(d_2 - sigma2, 0.0) / h2)

def __precise_edges(p: Pixel, height, width, offset_length):
    precise_p: Pixel = Pixel(p.x, p.y)

    if p.x - offset_length < 0:
        precise_p.x = offset_length
    if p.y - offset_length < 0:
        precise_p.y = offset_length

    if p.x + offset_length >= width:
        precise_p.x = width - offset_length - 1
    if p.y + offset_length >= height:
        precise_p.y = height - offset_length - 1

    return precise_p


def __generate_q_patches_arr(p: Pixel, arr_size) -> []:
    q_patch_arr = []
    r_range = 2 * NLMeans.r - 2 * NLMeans.f
    for q_number in range(arr_size):
        q_patch_arr.append(Pixel(p.x + random.randint(0, r_range) - r_range // 2,
                                 p.y + random.randint(0, r_range) - r_range // 2))

    return q_patch_arr


def multi_2d(input_tuple):
    vd_slice, height, width, sigma, z = input_tuple
    denoise_arr = vd_slice.copy()
    for y in range(height):
        for x in range(width):
            p = Pixel(x, y)
            p_offset_r = __precise_edges(p, height, width, NLMeans.r)
            p_offset_f = __precise_edges(p, height, width, NLMeans.f)
            q_arr = __generate_q_patches_arr(p_offset_r, NLMeans.Q_ARR_SIZE)

            c: float = 1.0
            nl_u: float = vd_slice[p.y][p.x]
            for q in q_arr:
                weight = weight_2d(p_offset_f, q, vd_slice, sigma)
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

    r = 22

    f =  6

    def __init__(self, data: np.ndarray, sigma: float):
        super().__init__(data)
        self.sigma = sigma

        self.h: int = 0.4 * sigma


    def execute_2d(self):
        data = self.data
        length, width, height = self.length, self.width, self.height
        denoise_arr: np.ndarray = np.zeros((length, height, width), 'f4')

        input_data = []
        for z in range(length):
            input_data.append((data[z], height, width, self.sigma, z))

        p = multiprocessing.Pool(multiprocessing.cpu_count())
        #p = multiprocessing.Pool(1)
        slices_map = p.map(multi_2d, input_data)

        for z in range(length):
            denoise_arr[z] = slices_map[z]

        return denoise_arr

