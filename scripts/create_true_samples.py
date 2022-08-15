import numpy as np
from scenarios import EMD_2984, _4NRE, EMD_3061, EMD_6479
from scripts import get_project_root
from scripts.ed_parser import read

# ed = read(str(get_project_root().parent) + EMD_2984)
# ed_help = read(str(get_project_root().parent) + '/results/best/EMD-2984_bm4d.ccp4')
# ed.re_normalize()
#
# thr_main = ed.header.mean + 1.2 * ed.header.stddev
# thr_help = ed_help.header.mean + ed_help.header.stddev
#
# true_signal = np.zeros((ed.header.fields["NS"] * ed.header.fields["NR"] * ed.header.fields["NC"]), dtype=bool)
#
# n = len(ed.buffer)
#
# for i in range(n):
#     if ed.buffer[i] >= thr_main and ed_help.buffer[i] >= thr_help:
#         true_signal[i] = True
#
# true_signal.tofile('EMD-2984')


if __name__ == '__main__':

    name ='EMD-2984'
    ed = read(str(get_project_root().parent) + '/mol_data/ccp4/vv2.ccp4')

    ed.re_normalize()

    true_signal = np.zeros((ed.header.fields["NS"] * ed.header.fields["NR"] * ed.header.fields["NC"]), dtype=bool)

    n = len(ed.buffer)

    for i in range(n):
        if ed.buffer[i] > 0.0:
            true_signal[i] = True

    true_signal.tofile(str(get_project_root().parent) + '/results/golden/' + name)