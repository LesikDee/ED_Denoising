from scripts import get_project_root
from scripts.ed_parser import read
from scripts.f_measure import make_f_measure_report
import numpy as np

bm3d_path = '_bm3d.ccp4'
mf2d_path = '_mf2d.ccp4'
nlm2d_path = '_nlm2d.ccp4'

bm4d_path = '_bm4d.ccp4'
mf3d_path = '_mf3d.ccp4'
nlm3d_path = '_nlm3d.ccp4'
origin = '_origin.ccp4'

def form_ed_tuple(ed_name, methods_names_tuple):
    ed_tuple = []
    for method_name in methods_names_tuple:
        file_path = str(get_project_root().parent) + '/results/best/' + ed_name + method_name
        ed = read(file_path)
        ed_tuple.append(ed)

    return ed_tuple

if __name__ == '__main__':
    ed_name = 'EMD-6479'
    true_buffer = np.fromfile(''.join([str(get_project_root().parent), '/results/golden/', ed_name, '_c']), dtype=bool)
    ed_tuple = form_ed_tuple(ed_name, [origin, mf3d_path, nlm3d_path, bm4d_path])

    make_f_measure_report(true_buffer, ed_tuple)
