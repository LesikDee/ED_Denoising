import scripts.ed_parser as parser

file_name = '../mol_data/dsn6/4nre_2fofc.dsn6'  # dsn6/4nre_2fofc.dsn6 ccp4/4nre.ccp4
file_path = file_name

mol_ed = parser.read(file_path)

# Step 2. Denoise by median filter
import denoise_methods.median_filter as mf
denoise_data = mf.median_filter(mol_ed.values)

from scripts.noise_signal_plot import build_graph
from scripts.edplot import edplot2d
mol_ed.update_values(new_values=denoise_data)
build_graph(mol_ed)
edplot2d(mol_ed)