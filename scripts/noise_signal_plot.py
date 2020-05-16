import numpy as np
import scripts.ed_parser as ed_parser
from matplotlib import pyplot
import scripts.model_core as mp
from scripts.molecule import MolRepresentation

# for ed map builds histogram: x axe - normalize density, y axe - amount of voxels with corresponding density
def build_graph(ed):
    ed.re_normalize()
    grid_number = 200
    n = len(ed.buffer)
    ed_arr = np.empty(grid_number, 'i4')
    for i in range(grid_number):
        ed_arr[i] = 0

    print('ed.buffer.min:', ed.buffer.min())
    print('ed.buffer.max:', ed.buffer.max())
    print('ed.header.mean:', ed.header.mean)
    print('ed.header.stddev:', ed.header.stddev)

    threshold = ed.header.mean + ed.header.stddev

    for i in range(n):
        val = int(ed.buffer[i] * (grid_number - 1))
        ed_arr[val] += 1


    x_axe = np.arange(0, grid_number)
    pyplot.figure()
    pyplot.plot(x_axe, ed_arr)

    pyplot.axvline(threshold * (grid_number - 1), color='g')

    print('threshold', threshold)
    pyplot.show()


def build_signal(ed_model: mp.Model):
    ed_model.execute_fc()
    ideal: MolRepresentation = ed_model.ed_fc
    ed: MolRepresentation = ed_model.ed_2fo_fc

    ideal.re_normalize()
    ed.re_normalize()

    data_length = len(ideal.buffer)
    signal_points_buf = np.empty(data_length, dtype=np.bool)

    threshold_ideal = ideal.header.mean + ideal.header.stddev
    print('threshold_ideal', threshold_ideal)
    grid_number = 400
    ed_ideal_arr = np.empty(grid_number, 'i4')
    ed_model_arr = np.empty(grid_number, 'i4')
    for i in range(grid_number):
        ed_ideal_arr[i] = 0
        ed_model_arr[i] = 0

    threshold = ed.header.mean + ed.header.stddev

    for i in range(data_length):
        signal_points_buf[i] = (ideal.buffer[i] >= threshold_ideal)
        val = int(ed.buffer[i] * (grid_number - 1))
        ed_model_arr[val] += 1
        if signal_points_buf[i]:
            ed_ideal_arr[val] += 1

    x_axe = np.arange(0, grid_number)
    pyplot.figure()
    pyplot.plot(x_axe, ed_model_arr, color='g')
    pyplot.plot(x_axe, ed_ideal_arr, color='b')
    pyplot.axvline(threshold * (grid_number - 1), color='r')
    pyplot.show()

if __name__ == '__main__':
    file_2fo_fc = '../mol_data/dsn6/4nre_2fofc.dsn6'
    file_fo_fc = '../mol_data/dsn6/4nre_fofc.dsn6'

    ed_2fo_fc = ed_parser.read(file_2fo_fc)
    ed_fo_fc = ed_parser.read(file_fo_fc)
    model = mp.Model(ed_2fo_fc, ed_fo_fc)

    build_signal(model)