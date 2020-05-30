import numpy as np
import matplotlib
from matplotlib import pyplot
from scripts.molecule import MolRepresentation

def print_stats(ed):
    print('Mean: {0} (calc: {1})'.format(ed.header.mean, np.mean(ed.values)))
    print('Std.Dev: {0} (calc: {1})'.format(ed.header.stddev, np.std(ed.values)))

def edplot2d(edfile: MolRepresentation, sec=-1, factor=1):
    if sec == -1:
        sec = edfile.header.nsec // 2
    edfile.re_normalize()

    values = edfile.values[sec]
    name = edfile.name.split('.')[0]
    #pyplot.figure()
    #pyplot.suptitle(name)
    fig, axes = pyplot.subplots(2, 2)
    fig.suptitle(name)
    crop_val = edfile.header.mean
    factor_list = [1, 1.5, 2, 2.5]
    for i in range(4):
        factor = factor_list[i]
        crop_min = edfile.header.mean - factor * edfile.header.stddev
        crop_max = edfile.header.mean + factor * edfile.header.stddev

        def crop(x):
            return crop_val if  x < crop_max else x

        values_cropped = np.vectorize(crop)(values)
        norm = matplotlib.colors.Normalize(crop_min, crop_max)
        #pyplot.subplot(2, 2, i + 1)
        axes[i // 2, i % 2].set_title('k = {0}'.format(factor))
        axes[i // 2, i % 2].imshow(values_cropped, cmap='bwr', norm=norm)

    for ax in fig.get_axes():
        ax.label_outer()
    pyplot.savefig(''.join(['../results/', name, '/sigma_level.png']))


    # pyplot.figure()
    # pyplot.suptitle(name)
    # pyplot.subplot(2, 2, 1)
    #pyplot.imshow(values, cmap='gray')
    # pyplot.subplot(2, 2, 2)
    # pyplot.imshow(values, cmap='bwr', norm=norm)
    # pyplot.subplot(2, 2, 3)
    # pyplot.imshow(values_cropped, cmap='gray')
    # pyplot.subplot(2, 2, 4)
    # pyplot.imshow(values_cropped, cmap='bwr', norm=norm)
    # pyplot.show()