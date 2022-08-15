from scripts import get_project_root
from scenarios import EMD_2984, _4NRE, EMD_3061, EMD_6479, _4XN6
from scripts.noise_signal_plot import write_stats
from scripts.ed_parser import read

if __name__ == '__main__':

    file_names = [_4NRE]
    for name in file_names:
        file_path = str(get_project_root().parent) + name

        ed = read(file_path)

        write_stats(ed)
        print('ok')
