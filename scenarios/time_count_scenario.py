import time
import denoise_methods.nl_means3d as nlm
import denoise_methods.BM4D as bm4d

from scripts.ed_parser import read
from scripts import get_project_root
from scenarios import EMD_2984, _4NRE, EMD_3061, EMD_6479

if __name__ == '__main__':
    file_path = str(get_project_root().parent) + EMD_2984
    ed = read(file_path)

    start = time.time()
    ed.re_normalize()
    ed.update_from_buffer(ed.buffer)
    denoiser = nlm.NLMeans(ed.values, 40)
    denoise_data = denoiser.execute_3d()

    finish = time.time()

    print('NL-means:' + str(finish - start))



    ed = read(file_path)

    start = time.time()
    ed.re_normalize()
    ed.update_from_buffer(ed.buffer)
    denoiser = bm4d.BM4D(ed.values, 40)
    denoise_data = denoiser.execute_3d()

    finish = time.time()

    print('BM4D:' + str(finish - start))
