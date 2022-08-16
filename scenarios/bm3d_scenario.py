from scripts.ed_parser import read
from scripts import get_project_root
from scripts.ccp4_parser import to_ccp4_file
from scripts import edplot
import denoise_methods.BM3D as BMND
import numpy as np
from scenarios import EMD_2984, _4NRE, EMD_3061, EMD_6479

if __name__ == '__main__':
    file_names = [EMD_6479] #, file_name2]
    for name in file_names:
        file_path = str(get_project_root().parent) + name

        ed = read(file_path)

        ed.re_normalize()
        denoiser = BMND.BM3D(ed.values)
        denoise_data = denoiser.execute_2d()

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
        to_ccp4_file(ed, 'bm3d_new')