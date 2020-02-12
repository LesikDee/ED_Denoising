import os
import sys
import numpy as np
import matplotlib
from matplotlib import pyplot
import dsn6_parser
import ccp4_parser


def print_stats(ed):
    print('Mean: {0} (calc: {1})'.format(ed.header.mean, np.mean(ed.values)))
    print('Std.Dev: {0} (calc: {1})'.format(ed.header.stddev, np.std(ed.values)))


def edplot2d(edfile, sec, factor=1):
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


def main(filename: str, sec=None):
    file_type = filename.split('.').pop()
    if file_type == 'dsn6':
        ed = dsn6_parser.read(filename)
    elif file_type == 'ccp4':
        ed = ccp4_parser.read(filename)
    else:
        raise TypeError
    print_stats(ed)
    if sec is None:
        sec = ed.header.nsec // 2
    edplot2d(ed, sec)


if __name__ == '__main__':
    path = '../mol_data/dsn6/4NRE.dsn6'  # '../mol_data/ccp4/4NRE.ccp4'  ../mol_data/dsn6/4NRE.dsn6
    # if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
    #     print('usage: %s <file.ccp4> [section]' % os.path.basename(sys.argv[0]))
    #     exit(-1)
    main(path, int(sys.argv[2]) if len(sys.argv) > 2 else None)
