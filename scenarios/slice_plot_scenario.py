# Step 1. Read data
from scripts.ed_parser import read
from scripts import get_project_root

file_name = '/mol_data/ccp4/EMD-2984.ccp4'  # dsn6/4nre_2fofc.dsn6 ccp4/4nre.ccp4
file_path = str(get_project_root().parent) + file_name
ed = read(file_path)

#Step 3. Plot slice
from scripts.edplot import edplot2d
edplot2d(ed)