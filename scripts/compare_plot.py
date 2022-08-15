import numpy as np
import matplotlib
matplotlib.rcParams.update({'font.size': 18})
from matplotlib import pyplot
import matplotlib.colors  as mcolors
from scripts import ed_parser
from scenarios import EMD_2984, _4NRE, EMD_3061, EMD_6479
from scripts.ed_parser import read
from scripts import get_project_root

def edplot2d(true_buffer, edfile_tuple,  factor=1, optName = 'file'):
    edfile = edfile_tuple[0]
    header = edfile.header
    sec = header.nsec // 2
    true_val = np.ndarray((header.fields["NS"], header.fields["NR"], header.fields["NC"]), 'bool', buffer=true_buffer)
    true_val_sec = true_val[sec]
    name = edfile.name.split('.')[0]
    name_tuple = ['Origin', 'MF', 'NL-Means','BM4D']

    fig, axes = pyplot.subplots(2, 2)
    fig.suptitle(name)

    for k in range(len(edfile_tuple)):
        edfile = edfile_tuple[k]
        slice_sec = edfile.values[sec]
        thr =  edfile.header.mean +  edfile.header.stddev
        n = len(slice_sec)
        m = len(slice_sec[0])
        new_slice_sec = np.ndarray((n,m,3))
        for i in range(n):
            for j in range(m):
                new_slice_sec[i][j] = [1.0, 0.0, 0.0]
                if slice_sec[i][j] >= thr:
                    if not true_val_sec[i][j]:
                        new_slice_sec[i][j] = [0.0, 0.0, 1.0]
                        #print('FN')
                else:
                    if  true_val_sec[i][j]:
                        new_slice_sec[i][j] = [1/255, 215/255, 36/255]
                        #print('FP')
                    else:
                        new_slice_sec[i][j] = [1.0, 1.0, 1.0]


        axes[k // 2, k % 2].set_title(name_tuple[k])
        axes[k // 2, k % 2].imshow(new_slice_sec)

    for ax in fig.get_axes():
        ax.label_outer()
        # pyplot.subplot(2, 2, k + 1)
        # pyplot.imshow(new_slice_sec)


    pyplot.show()

    #pyplot.savefig(''.join(['../results/', name, '/', optName ,'.png']))


if __name__ == '__main__':

    file = EMD_2984
    ed_name = 'EMD-2984'
    true_buffer = np.fromfile(''.join([str(get_project_root().parent), '/results/golden/', ed_name + '_c']), dtype=bool)
    origin = ed_parser.read(str(get_project_root().parent) + file)
    origin.re_normalize()
    mf3d = ed_parser.read(str(get_project_root().parent) + '/results/best/' + ed_name +'_mf3d.ccp4')
    nlm3d = ed_parser.read(str(get_project_root().parent) + '/results/best/' + ed_name + '_nlm3d.ccp4')
    bm4d = ed_parser.read(str(get_project_root().parent) + '/results/best/' + ed_name + '_bm4d.ccp4')
    edplot2d(true_buffer, [origin, mf3d, nlm3d, bm4d])