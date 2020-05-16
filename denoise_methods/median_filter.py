import numpy as np

def median_filter(vd_3d_input: np.ndarray, window3d_size = 3):
    length = len(vd_3d_input)
    height = len(vd_3d_input[0])
    width = len(vd_3d_input[0][0])
    print(height, width, length)
    denoise_arr: np.ndarray = vd_3d_input.copy()
    edge = window3d_size // 2

    for x in range(edge, width - edge):
        for y in range(edge, height - edge):
            for z in range(edge, length - edge):
                cube_data = []
                for i in range(window3d_size):
                    for j in range(window3d_size):
                        for k in range(window3d_size):
                            cube_data.append(vd_3d_input[z + k  - edge][y + j - edge][x + i - edge])

                cube_data.sort()
                denoise_arr[z][y][x] = cube_data[window3d_size * window3d_size * window3d_size // 2]

    return denoise_arr