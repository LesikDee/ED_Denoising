from scripts.ed_parser import read
from scripts import get_project_root
from scripts.ccp4_parser import to_ccp4_file

import numpy as np
from scenarios import EMD_2984, _4NRE, EMD_3061, EMD_6479, EMD_21452
import denoise_methods.BM4D as BM4D

if __name__ == '__main__':
    name = EMD_21452
    threshold_list = [5.25]
    for tr in threshold_list:
        file_path = str(get_project_root().parent) + name

        ed = read(file_path)

        ed.re_normalize()
        denoiser = BM4D.BM4D(ed.values)
        denoise_data = denoiser.execute_3d(tr)

        ed.update_from_values(denoise_data)
        ed.header.mean = np.mean(ed.buffer)
        ed.header.stddev = np.std(ed.buffer)
        ed.header.min = np.min(ed.buffer)
        ed.header.max = np.max(ed.buffer)

        ed.header.fields["amean"] = ed.header.mean
        ed.header.fields["amax"] = ed.header.max
        ed.header.fields["amin"] = ed.header.min
        ed.header.fields["sd"] = ed.header.stddev

        print(ed.header.min, ed.header.max, ed.header.mean, ed.header.stddev)
        to_ccp4_file(ed, 'bm4d_14p_' + str(tr))

