from .denoise_method import *
import random
import numpy
import multiprocessing

def distance2_2d(p: Pixel, q: Pixel, vd_slice, patch_size):
    dist_m = vd_slice[p.y: p.y + patch_size, p.x: p.x + patch_size] - \
             vd_slice[q.y: q.y + patch_size, q.x: q.x + patch_size]

    dist_2 = np.sum(dist_m ** 2)
    return 1000.0 * dist_2 / (2 * patch_size + 1) ** 2

# current_p - left upper patch pixel
class Area:
    def __init__(self, current_p: Pixel, height: int, width: int, area_size, window_size):
        p_start_x =  current_p.x - area_size // 2 + window_size // 2
        if p_start_x < 0:
            p_start_x = 0

        if p_start_x + area_size + window_size >= width:
            p_start_x = width - area_size - window_size - 1

        p_start_y =  current_p.y - area_size // 2 + window_size // 2
        if p_start_y < 0:
            p_start_y = 0

        if p_start_y + area_size + window_size >= height:
            p_start_y = height - area_size - window_size  - 1

        self.start: Pixel = Pixel(x=p_start_x, y=p_start_y)
        self.end: Pixel =Pixel(x=p_start_x + area_size, y=p_start_y+ area_size)



def multi_2d(input_tuple):
    slice_2d, height, width, z = input_tuple[0], input_tuple[1], input_tuple[2], input_tuple[3]
    used_patches = numpy.zeros((height, width), dtype=bool)
    numerator_slice = numpy.copy(slice_2d)
    denum_slice = numpy.ones((height, width), dtype='f4')
    y_finish, y = False, 0
    while not y_finish:
        if y > height - BMnD.PATCH_SIZE:
            y = height - BMnD.PATCH_SIZE - 1
            y_finish = True

        x_finish, x = False, 0
        while not x_finish:
            if x > width - BMnD.PATCH_SIZE:
                x = width - BMnD.PATCH_SIZE - 1
                x_finish = True


            p = Pixel(x, y)
            group_list = BMnD.grouping_2d(slice_2d, p, height, width, used_patches)
            block, block_place = group_list[0], group_list[1]

            block_depth = len(block_place)
            if block_depth > 1:

                block_filtered = BMnD.filtering_2d(block)

                # aggregation
                for block_z in range(block_depth):
                    y_place = block_place[block_z].y
                    x_place = block_place[block_z].x
                    numerator_slice[y_place: y_place + BMnD.PATCH_SIZE, x_place: x_place + BMnD.PATCH_SIZE] \
                        += block_filtered[block_z]

                    denum_slice[y_place: y_place + BMnD.PATCH_SIZE, x_place: x_place + BMnD.PATCH_SIZE] \
                        += 1.0

            x += BMnD.PATCH_STEP

        y += BMnD.PATCH_STEP

    numerator_slice /= denum_slice
    print(z)
    return numerator_slice

class BMnD(DenoiseMethod):

    PATCH_SIZE = 8

    PATCH_STEP = 4

    MAX_FIND_STEPS = 30

    MATCH_AREA_SIZE = 36

    def __init__(self, data: np.ndarray, sigma: float = 0):
        super().__init__(data)
        self.sigma = sigma

    @staticmethod
    def grouping_2d(data: np.ndarray, patch_p: Pixel, height, width, used_patches: np.ndarray):
        block_index = [patch_p]
        dist_list = [0.0]
        used_patches[patch_p.y][patch_p.x] = True

        search_area = Area(patch_p, height, width, BMnD.MATCH_AREA_SIZE, BMnD.PATCH_SIZE)

        find_steps = 0
        while find_steps <= BMnD.MAX_FIND_STEPS:
            find_steps += 1

            potential_patch = Pixel(random.randint(search_area.start.x, search_area.end.x),
                                                     random.randint(search_area.start.y, search_area.end.y))

            # if used_patches[potential_patch.y][potential_patch.x]:
            #     continue

            dist = distance2_2d(patch_p, potential_patch, data, BMnD.PATCH_SIZE)

            if dist < 0.5:
                used_patches[potential_patch.y][potential_patch.x] = True
                # insert
                i = 0
                while i < len(block_index) and dist > dist_list[i]:
                    i += 1
                block_index.insert(i, potential_patch)
                dist_list.insert(i, dist)

            if len(block_index) == BMnD.PATCH_SIZE:
                break

        #print(dist_list)
        # form 3d array block
        block = np.ndarray((len(block_index), BMnD.PATCH_SIZE, BMnD.PATCH_SIZE), dtype='f4')
        in_p = 0
        for p in block_index:
            block[in_p] = data[p.y: p.y +  BMnD.PATCH_SIZE, p.x: p.x +  BMnD.PATCH_SIZE]
            in_p += 1

        return [block, block_index]

    @staticmethod
    def filtering_2d(block: np.ndarray):
        z_block = len(block)
        filtered_block = np.zeros((z_block, BMnD.PATCH_SIZE, BMnD.PATCH_SIZE), dtype='f4')

        for z in range(z_block):
            sum_weight = 0
            for n in range(z_block):
                dist = abs(n - z - 1)
                weight = 0.2 if dist > 3 else 1.0 / 2.0 ** dist

                filtered_block[z] += weight * block[n]
                sum_weight += weight

            filtered_block[z] /= sum_weight

        return filtered_block

    #bm3d
    def execute_2d(self):
        length, width, height = self.length, self.width, self.height

        denoise_arr: np.ndarray = np.zeros((length, width, height), 'f4')

        input_data = []
        for z in range(length):
            input_data.append((self.data[z], height, width, z))

        p = multiprocessing.Pool(multiprocessing.cpu_count())
        slices_map = p.map(multi_2d, input_data)

        for z in range(length):
            denoise_arr[z] = slices_map[z]

        return denoise_arr