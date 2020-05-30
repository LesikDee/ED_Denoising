# Step 1. Read data
from scripts.ed_parser import read
from scripts import get_project_root

file_name = '/mol_data/ccp4/4nre.ccp4'  # dsn6/4nre_2fofc.dsn6 ccp4/4nre.ccp4 EMD-6479.ccp4
file_path = str(get_project_root().parent) + file_name
ed = read(file_path)

# Step 2. Build histogram
from scripts.noise_signal_plot import build_graph
build_graph(ed)
