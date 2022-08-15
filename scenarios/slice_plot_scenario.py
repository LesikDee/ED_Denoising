# Step 1. Read data
from scripts.ed_parser import read
from scripts import get_project_root
from scenarios import EMD_2984, _4NRE, EMD_3061, EMD_6479


ed = read(str(get_project_root().parent) + _4NRE)
ed.re_normalize()
#Step 3. Plot slice
from scripts.edplot import edplot2d
edplot2d(ed, optName='slice_color')