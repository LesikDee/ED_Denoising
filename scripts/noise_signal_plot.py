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

    # print('ed.buffer.min:', ed.buffer.min())
    # print('ed.buffer.max:', ed.buffer.max())
    # print('ed.header.mean:', ed.header.mean)
    print('ed.header.stddev:', ed.header.stddev)

    threshold = ed.header.mean + ed.header.stddev

    for i in range(n):
        val = int(ed.buffer[i] * (grid_number - 1))
        ed_arr[val] += 1

    x_axe = np.linspace(0.0, 1.0, num=grid_number)

    pyplot.figure()

    name = ed.name.split('.')[0]
    pyplot.suptitle(name)
    pyplot.plot(x_axe, ed_arr)
    pyplot.axvline(threshold, color='g')

    #print('threshold', threshold)
    #pyplot.show()

    pyplot.savefig(''.join(['../results/',name,'/histogram.png']))

def write_stats(ed: MolRepresentation, file_type = '_stats'):
    ed.re_normalize()
    name = ed.name.split('.')[0]
    with open(''.join(['../results/',name,'/', name,  file_type ,'.txt']), 'w') as f:
        f.write('mean ' + str(ed.header.mean) + '\n')
        f.write('sd ' + str(ed.header.stddev) + '\n')

        n = len(ed.buffer)

        threshold = ed.header.mean + ed.header.stddev
        noise_elm_count = 0
        signal_elm_count = 0

        for elm in ed.buffer:
            if elm >= threshold:
                signal_elm_count += 1
            else:
                noise_elm_count += 1

        f.write('Signal elements number: ' + str(signal_elm_count) + '\n')
        f.write('Noise elements number: ' + str(noise_elm_count) + '\n')
        f.write('All elements number: ' + str(noise_elm_count + signal_elm_count) + '\n')
        f.write('Ratio: ' + str(signal_elm_count / (noise_elm_count + signal_elm_count) ) + '\n')


