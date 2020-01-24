import sys
import os
import numpy as np
import ccp4_parser
import dsn6_parser
from matplotlib import pyplot
import math


def build_graph(ed):
    grid_number = 100
    n = len(ed.data)
    ed_arr = np.empty(grid_number, 'i4')
    for i in range(grid_number):
        ed_arr[i] = 0

    max_val = math.fabs(ed.data.max()) if math.fabs(ed.data.max()) > math.fabs(ed.data.min()) else math.fabs(ed.data.min())
    ed.data /= max_val

    # mean = 0
    # for i in range(n):
    #     mean += ed.data[i]
    # mean /= n
    # stddev = 0
    # for i in range(n):
    #     stddev += (ed.data[i] - mean) ** 2
    # stddev = (stddev / n) ** 0.5
    # print(mean, stddev)

    for i in range(n):
        val = int((ed.data[i] + 1) / 2 * (grid_number - 1))
        ed_arr[val] += 1

    x_axe = np.arange(0, grid_number)
    pyplot.figure()
    pyplot.plot(x_axe, ed_arr)
    pyplot.axvline((ed.data.max() - ed.header.mean + ed.header.stddev) / (ed.data.max() - ed.data.min()) * (grid_number - 1),
                   color='g')
    pyplot.show()


if __name__ == '__main__':
    file = '../mol_data/dsn6/4xn6_2fofc.dsn6'

    if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
        file = sys.argv[1]

    ed = dsn6_parser.read(file)
    build_graph(ed)
