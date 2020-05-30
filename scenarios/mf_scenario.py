# Step 1. Read data
from scripts.ed_parser import read
from scripts import get_project_root
from scripts.ccp4_parser import to_ccp4_file
from scripts import edplot
import numpy as np
file_name = '/mol_data/ccp4/EMD-6479.ccp4'  # dsn6/4nre_2fofc.dsn6 ccp4/4nre.ccp4
file_path = str(get_project_root().parent) + file_name
ed = read(file_path)

import denoise_methods.median_filter as mf
denoiser = mf.MedianFilter(ed.values)
denoise_data = denoiser.execute_3d()

#ed.values = denoise_data
ed.update_from_values(denoise_data)
ed.header.mean = np.mean(ed.buffer)
ed.header.stddev = np.std(ed.buffer)
ed.header.min = np.min(ed.buffer)
ed.header.max = np.max(ed.buffer)


ed.header.fields["amean"] = ed.header.mean
ed.header.fields["amax"] = ed.header.max
ed.header.fields["min"] = ed.header.min
ed.header.fields["sd"] = ed.header.stddev

print(ed.header.min, ed.header.max, ed.header.mean, ed.header.stddev)
#ed.re_normalize()
edplot.edplot2d(ed)

to_ccp4_file(ed, 'mf_3d')
