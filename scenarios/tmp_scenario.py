import numpy as np
import multiprocessing

def create_arr(size):
    arr = np.ndarray((size,size,size))
    for k in range(0, patch_size):
        for j in range(0, patch_size):
            for i in range(0, patch_size):
                arr[k][j][i] = i + j + k
    return arr



if __name__ == '__main__':
    patch_size = 4
    arr1 = create_arr(patch_size)
    arr2 = np.ones((patch_size,patch_size,patch_size))

    dist = 0
    for k in range(0, patch_size):
        for j in range(0, patch_size):
            for i in range(0, patch_size):
                diff = arr1[k][j][i] - arr2[k][j][i]
                dist += diff * diff

    print(dist)

    arr3 = arr1 - arr2
    print(np.sum(arr3**2))