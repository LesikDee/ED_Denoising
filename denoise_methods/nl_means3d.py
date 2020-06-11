import math
from .denoise_method import *
import random
import multiprocessing

def distance2_3d(p: Voxel, q: Voxel, data):
    f = NLMeans.f
    dist_m = data[p.z - f: p.z + f + 1, p.y - f: p.y + f + 1, p.x - f: p.x + f + 1] - \
             data[q.z - f: q.z + f + 1, q.y - f: q.y + f + 1 , q.x - f: q.x + f + 1]

    dist_2 = np.sum(dist_m ** 2)
    return dist_2 / (2 * f + 1) ** 3

def weight(p: Voxel, q: Voxel, data, sigma) -> float:
    #h = 0.2 * sigma
    h = 16 * sigma
    d_2 = distance2_3d(p, q, data) * 2.5 * 10e8
    #print(d_2, d_2 - 2 * sigma * sigma,  math.e ** -(max(d_2 - 2 * sigma * sigma, 0.0) / (h * h)))
    return math.e ** -(max(d_2 - 2 * sigma * sigma, 0.0) / (h * h))

def __precise_edges(p: Voxel, length, height, width, offset_length):
    precise_p: Voxel = Voxel(p.x, p.y, p.z)
    
    if p.x - offset_length < 0:
        precise_p.x = offset_length
    if p.y - offset_length < 0:
        precise_p.y = offset_length
    if p.z - offset_length < 0:
        precise_p.z = offset_length

    if p.x + offset_length >= width:
        precise_p.x = width - offset_length - 1
    if p.y + offset_length >= height:
        precise_p.y = height - offset_length - 1
    if p.z + offset_length >= length:
        precise_p.z = length - offset_length - 1

    return precise_p


def __generate_q_patches_arr(p: Voxel, arr_size) -> []:
    q_patch_arr = []
    r_range = 2 * NLMeans.r - 2 * NLMeans.f
    for q_number in range(arr_size):
        q_patch_arr.append(Voxel(p.x + random.randint(0, r_range) - r_range // 2,
                                 p.y + random.randint(0, r_range) - r_range // 2,
                                 p.z + random.randint(0, r_range) - r_range // 2
                                 ))

    return q_patch_arr


def multi_3d(input_tuple):
    data, length, height, width, sigma, z = input_tuple
    denoise_arr = data[z].copy()
    for y in range(height):
        for x in range(width):
            p = Voxel(x, y, z)
            p_offset_r = __precise_edges(p, length, height, width, NLMeans.r)
            p_offset_f = __precise_edges(p, length, height, width, NLMeans.f)
            q_arr = __generate_q_patches_arr(p_offset_r, NLMeans.Q_ARR_SIZE)

            c: float = 1.0
            nl_u: float = data[p.z][p.y][p.x]
            for q in q_arr:
                weight_q = weight(p_offset_f, q, data, sigma)
                c += weight_q
                nl_u += data[q.z][q.y][q.x] * weight_q

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


    def execute_3d(self):
        data = self.data
        length, width, height = self.length, self.width, self.height
        denoise_arr: np.ndarray = np.zeros((length,height, width), 'f4')

        input_data = []
        for z in range(length):
            input_data.append((data, length, height, width, self.sigma, z))

        p = multiprocessing.Pool(multiprocessing.cpu_count())
        #p = multiprocessing.Pool(1)
        slices_map = p.map(multi_3d, input_data)

        for z in range(length):
            denoise_arr[z] = slices_map[z]

        return denoise_arr

