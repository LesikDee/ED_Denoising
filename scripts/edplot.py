import numpy as np
import matplotlib
from matplotlib import pyplot

def print_stats(ed):
    print('Mean: {0} (calc: {1})'.format(ed.header.mean, np.mean(ed.values)))
    print('Std.Dev: {0} (calc: {1})'.format(ed.header.stddev, np.std(ed.values)))

def edplot2d(edfile, sec=-1, factor=1):
    if sec == -1:
        sec = edfile.header.nsec // 2

    crop_val = edfile.header.mean
    crop_min = edfile.header.mean - factor * edfile.header.stddev
    crop_max = edfile.header.mean + factor * edfile.header.stddev

    def crop(x):
        return crop_val if crop_min < x < crop_max else x

    values = edfile.values[sec]
    values_cropped = np.vectorize(crop)(values)
    norm = matplotlib.colors.Normalize(crop_min, crop_max)

    pyplot.figure()
    pyplot.suptitle(edfile.name)
    pyplot.subplot(2, 2, 1)
    pyplot.imshow(values, cmap='gray')
    pyplot.subplot(2, 2, 2)
    pyplot.imshow(values, cmap='bwr', norm=norm)
    pyplot.subplot(2, 2, 3)
    pyplot.imshow(values_cropped, cmap='gray')
    pyplot.subplot(2, 2, 4)
    pyplot.imshow(values_cropped, cmap='bwr', norm=norm)
    pyplot.show()
