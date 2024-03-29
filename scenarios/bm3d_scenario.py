# Step 1. Read data
from scripts.ed_parser import read
from scripts import get_project_root
from scripts.ccp4_parser import to_ccp4_file
from scripts import edplot
import numpy as np

if __name__ == '__main__':
    file_name1 = '/mol_data/ccp4/EMD-3061.ccp4'  # dsn6/4nre_2fofc.dsn6 ccp4/4nre.ccp4 EMD-3061 EMD-6479
    file_name2 = '/mol_data/ccp4/EMD-6479.ccp4'
    file_names = [file_name2] #, file_name2]
    for name in file_names:
        file_path = str(get_project_root().parent) + name

        ed = read(file_path)

        import denoise_methods.BM3D as BMND


        ed.re_normalize()
        denoiser = BMND.BMnD(ed.values, 40)
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
        #ed.re_normalize()
        #edplot.edplot2d(ed,optName='bm3d_')
        #edplot.edplot2d(ed, optName='true1')
        to_ccp4_file(ed, 'bm3d_2')