import numpy as np
import multiprocessing

def runner(tuple_data):
    arr_2d, k = tuple_data[0], tuple_data[1]
    print()
    for i in range(8):
        for j in range(8):
            arr_2d[i][j] = i + j

    return k



if __name__ == '__main__':
    a = np.zeros((8, 8, 8), 'f4')
    input_data = []
    for k in range(8):
        input_data.append((a[k], k))
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    z = p.map(runner, input_data)
    print(z)