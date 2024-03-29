# Step 1. Read data
from scripts.ed_parser import read
from scripts import get_project_root
from scripts.ccp4_parser import to_ccp4_file
from scripts import edplot
import numpy as np
from scenarios import EMD_2984, _4NRE, EMD_3061, EMD_6479

if __name__ == '__main__':
    file_names = [_4NRE]
    for name in file_names:
        file_path = str(get_project_root().parent) + name
        ed = read(file_path)

        import denoise_methods.nl_means as nlm

        ed.re_normalize()
        ed.update_from_buffer(ed.buffer)
        denoiser = nlm.NLMeans(ed.values, 40)
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

        #print('++++++', ed.header.min, ed.header.max, ed.header.mean, ed.header.stddev)
        #ed.re_normalize()
        #edplot.edplot2d(ed, optName='nlm_2d')

        to_ccp4_file(ed, 'nlm_2d_v2')