from .denoise_method import *
import random
import numpy


def distance3d(p: Voxel, q: Voxel, data, patch_size):
    dist_m = data[p.z: p.z + patch_size, p.y: p.y + patch_size, p.x: p.x + patch_size] - \
             data[q.z: q.z + patch_size, q.y: q.y + patch_size, q.x: q.x + patch_size]

    dist_2 = np.sum(dist_m ** 2)
    return 1000.0 * dist_2 / (patch_size * patch_size * patch_size)

# current_p - left upper patch pixel
class Area3D:
    def __init__(self, current_p: Voxel, length: int, height: int, width: int, area_size, window_size):
        p_start_x =  current_p.x - area_size // 2 + window_size // 2
        if p_start_x < 0:
            p_start_x = 0

        if p_start_x + area_size + window_size >= width:
            p_start_x = width - area_size - window_size

        p_start_y =  current_p.y - area_size // 2 + window_size // 2
        if p_start_y < 0:
            p_start_y = 0

        if p_start_y + area_size + window_size >= height:
            p_start_y = height - area_size - window_size

        p_start_z =  current_p.z - area_size // 2 + window_size // 2
        if p_start_z < 0:
            p_start_z = 0

        if p_start_z + area_size + window_size >= length:
            p_start_z = length - area_size - window_size

        self.start: Voxel = Voxel(x=p_start_x, y=p_start_y, z=p_start_z)
        self.end: Voxel = Voxel(x=p_start_x + area_size, y=p_start_y+ area_size, z=p_start_z+ area_size)


def multi_3d(input_tuple):
    data, length, height, width, tr = input_tuple

    numerator_slice = numpy.copy(data)
    denum_slice = numpy.ones((length, height, width), dtype='f4')

    z_finish, z = False, 0
    while not z_finish:
        if z >= length - BM4D.PATCH_SIZE:
            z = length - BM4D.PATCH_SIZE - 1
            z_finish = True

        y_finish, y = False, 0
        while not y_finish:
            if y >= height - BM4D.PATCH_SIZE:
                y = height - BM4D.PATCH_SIZE - 1
                y_finish = True

            x_finish, x = False, 0
            while not x_finish:
                if x >= width - BM4D.PATCH_SIZE:
                    x = width - BM4D.PATCH_SIZE - 1
                    x_finish = True

                p = Voxel(x, y, z)
                group_list = BM4D.grouping_3d(data, p, length, height, width, tr)
                block, block_place = group_list[0], group_list[1]

                block_depth = len(block_place)
                if block_depth > 1:

                    block_filtered = BM4D.filtering_3d(block)

                    # aggregation
                    for block_4d in range(block_depth):
                        y_place = block_place[block_4d].y
                        x_place = block_place[block_4d].x
                        z_place = block_place[block_4d].z
                        numerator_slice[z_place: z_place + BM4D.PATCH_SIZE, y_place: y_place + BM4D.PATCH_SIZE,
                            x_place: x_place + BM4D.PATCH_SIZE]  += block_filtered[block_4d]

                        denum_slice[z_place: z_place + BM4D.PATCH_SIZE, y_place: y_place + BM4D.PATCH_SIZE,
                            x_place: x_place + BM4D.PATCH_SIZE] += 1.0

                x += BM4D.PATCH_STEP

            y += BM4D.PATCH_STEP

        #print(z)
        z += BM4D.PATCH_STEP

    numerator_slice /= denum_slice
    return numerator_slice

class BM4D(DenoiseMethod):

    PATCH_SIZE = 16

    PATCH_STEP = 5

    MAX_FIND_STEPS = 30

    MATCH_AREA_SIZE = 44

    def __init__(self, data: np.ndarray, sigma: float = 0):
        super().__init__(data)
        self.sigma = sigma

    @staticmethod
    def grouping_3d(data: np.ndarray, patch_p: Voxel, length, height, width, tr = 1.0):
        block_index = [patch_p]
        dist_list = [0.0]

        search_area = Area3D(patch_p, length, height, width, BM4D.MATCH_AREA_SIZE, BM4D.PATCH_SIZE)

        find_steps = 0
        while find_steps <= BM4D.MAX_FIND_STEPS:
            find_steps += 1

            potential_patch = Voxel(random.randint(search_area.start.x, search_area.end.x),
                                    random.randint(search_area.start.y, search_area.end.y),
                                    random.randint(search_area.start.z, search_area.end.z))

            if patch_p.x == potential_patch.x and patch_p.y == potential_patch.y and patch_p.z == potential_patch.z:
                continue

            dist = distance3d(patch_p, potential_patch, data, BM4D.PATCH_SIZE)
            #print(dist)
            if dist < tr:
                i = 0
                while i < len(block_index) and dist > dist_list[i]:
                    i += 1
                block_index.insert(i, potential_patch)
                dist_list.insert(i, dist)

            if len(block_index) == BM4D.PATCH_SIZE + 1:
                block_index.pop()
                dist_list.pop()
                if find_steps == BM4D.MAX_FIND_STEPS // 1.5:
                    break

        #print(dist_list)

        # form 4d array block
        block = np.ndarray((len(block_index),BM4D.PATCH_SIZE, BM4D.PATCH_SIZE, BM4D.PATCH_SIZE), dtype='f4')
        in_p = 0
        for p in block_index:
            block[in_p] = data[p.z: p.z +  BM4D.PATCH_SIZE, p.y: p.y +  BM4D.PATCH_SIZE, p.x: p.x +  BM4D.PATCH_SIZE]
            in_p += 1

        return [block, block_index]

    @staticmethod
    def filtering_3d(block: np.ndarray):
        l_dir = len(block)
        filtered_block = np.zeros((l_dir, BM4D.PATCH_SIZE, BM4D.PATCH_SIZE, BM4D.PATCH_SIZE), dtype='f4')

        for l in range(l_dir):
            sum_weight = 0
            for n in range(l_dir):
                dist = abs(n - l - 1)
                weight = 0.2 if dist > 3 else 1.0 / 2.0 ** dist

                filtered_block[l] += weight * block[n]
                sum_weight += weight

            filtered_block[l] /= sum_weight

        return filtered_block

    #bm3d
    def execute_3d(self, tr = 1.0):
        length, width, height = self.length, self.width, self.height

        denoise_arr = multi_3d((self.data, length, height, width, tr))
        return denoise_arr