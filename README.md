# Electron density denoising algorithms implementation 
Implementation of noise reduction algorithms applying to electron density maps. This code is part of [master's qualification diploma](https://elib.spbstu.ru/dl/3/2020/vr/vr20-1604.pdf/en/info).
The purpose is to show how good BM4D (3d case of [BM3D (Block-matching and 3D filtering)](https://en.wikipedia.org/wiki/Block-matching_and_3D_filtering)) works with ed-maps.

#### Example of current implementation BM4D denoise algorithm applying to [EMD-2984 map](https://www.ebi.ac.uk/emdb/EMD-2984) visualized through [miew visualizer](https://miew.app).
![Miew – 3D Molecular Viewer - Google Chrome 2022-08-14 23-52-43_Segment_0_gif_008](https://user-images.githubusercontent.com/22669290/184553404-890da389-0adb-4dd1-9914-2c5e9c3e7aa5.gif)
![Miew – 3D Molecular Viewer - Google Chrome 2022-08-15 00-09-23_Segment_0_gif_003](https://user-images.githubusercontent.com/22669290/184553710-2a7382c4-0fbf-443e-817d-8df28a11c41e.gif)  
The left picture is the origin EMD-2984 map and the right picture is denoised by [current BM4D algorithm](https://github.com/LesikDee/ED_Denoising/blob/master/denoise_methods/BM4D.py) map. 

### How to check this out:
1. Open any molecular viewer in the first tab, suggested [miew](https://miew.app).
   - Load origin EMD-2984 map (in miew: open menu, choose load, load from file, chose EMD-2984_origin.ccp4 from [ED-maps-denoised-results](https://drive.google.com/file/d/1mYSBrdHIVrSlMNVcsnoMS7dYfFaJ06l4/view?usp=sharing) archive or from [emdb site](https://www.ebi.ac.uk/emdb/EMD-2984)).
2. Open molecular viewer in the second tab,
   - Load bm4d denoised map (in miew: open menu, choose load, load from file, choose [EMD-2984_bm4d.ccp4](https://drive.google.com/file/d/1jRJorxflOojTLKQzi0J8fyxSohO1mKd5/view?usp=sharing). 
   - Enable representing several molecules in the viewer, if not so by default (in miew: Open terminal (arrow in upper-left corner), write in terminal “set use.multiFile 1”)
   - Load “5a1a” PDB (it is PDB model of EMD-2984 map), (in miew: Open menu, choose load, write “5a1a”)
   - Additionally, for better view in miew: Open “Display mode” (upper-right) corner, choose balls mode

## State of the problem
Electron density maps can be viewed as single-channel 3D images indicating the density of a substance at each point (cell).
The vast majority of cells in molecular density maps are empty, that is, they are filled with noise.
If one visualize all the cells indiscriminately, one gets an almost uniform box in which nothing can be disassembled.
For the most part, the values of cells with a signal are higher than those of cells with noise.
Therefore, in order to visualize a signal, some threshold number is usually chosen (default: **expected value + 3 sigma**) 
and cells whose value is greater than the threshold number are considered as signal and are visualized, the rest are considered as noise and are not displayed.
However, it is not always easy to find such a threshold number, moreover, the values of some noisy cells exceed the threshold,
and such cells are visualized.  
**Proposed solution:**  
A model is proposed in which the ed-map is considered as a 3D image with white Gaussian noise superimposed. 
Then supposed to apply noise reduction algorithms to these maps.

## Implemented algorithms
- [Median filter](https://en.wikipedia.org/wiki/Median_filter) with 2d and 3d window.
- [Non-local means](https://en.wikipedia.org/wiki/Non-local_means) with 2d and 3d window.
- [Block-matching and 3D filtering (BM3D)](https://en.wikipedia.org/wiki/Non-local_means) and generalization to 3d input picture - BM4D.

For non-local means and BM3D-BM4D applying an approach to matching a random subset (not all, but a sufficient number) of matching blocks. This approach 
is based on [*Monte Carlo non local means: Random sampling for large-scale image filtering*](https://arxiv.org/abs/1312.7366) article.
The implementation of BM3D-BM4D is not entirely done (omitted second step with filtering in the spectral area). But just the first step already demonstrates satisfactory results.

## How to run
Code supported ccp4 (.map) and dsn6 formats of electron density maps. So there are
[ccp4](https://github.com/LesikDee/ED_Denoising/blob/add-readme/scripts/ccp4_parser.py) and
[dsn6](https://github.com/LesikDee/ED_Denoising/blob/add-readme/scripts/dsn6_parser.py) parsers accordingly.  
Class [MolRepresentation](https://github.com/LesikDee/ED_Denoising/blob/add-readme/scripts/molecule.py) consists of:
- 3-d NumPy array which is the content of ed-map
- header of ed-map (some additional meta information)
- statistics information (required for normalization)

1) Example of reading ccp4 ed-map:  
```python
from scripts.ed_parser import read
from scripts.molecule import MolRepresentation

filePath = 'EMD-6479.ccp4'
ed: MolRepresentation =  read(filePath)
```

2) Example of running denoising algorithm:  
```python
import denoise_methods.BM4D as BM4D

threshold = 4.85
ed.re_normalize()  # normalization is obligatory!
denoiser = BM4D.BM4D(ed.values)
denoise_data = denoiser.execute_3d(threshold)
```
3) Example of writing denoised data to file  
Denoise algorithms work only with 3d data (*ed.values*). So to save new data the easiest way is to use updated header information from the original map:
```python
from scripts.ccp4_parser import to_ccp4_file
import numpy as np

ed.update_from_values(denoise_data)
ed.header.mean = np.mean(ed.buffer)
ed.header.stddev = np.std(ed.buffer)
ed.header.min = np.min(ed.buffer)
ed.header.max = np.max(ed.buffer)

ed.header.fields["amean"] = ed.header.mean
ed.header.fields["amax"] = ed.header.max
ed.header.fields["amin"] = ed.header.min
ed.header.fields["sd"] = ed.header.stddev

to_ccp4_file(ed, 'bm4d')
```
## Results
To test denoise algorithms it is been taken several ed-maps with varying degrees of noise: [4NRE](https://www.rcsb.org/structure/4nre), [EMD-6479](https://www.ebi.ac.uk/emdb/EMD-6479), [EMD-2984](https://www.ebi.ac.uk/emdb/EMD-2984).  
Original maps and best results for each method (2d and 3d) are laid in [ED-maps-denoised-results](https://drive.google.com/file/d/1mYSBrdHIVrSlMNVcsnoMS7dYfFaJ06l4/view?usp=sharing) archive.

### Signal-noise slice representation
**Red**: True positive  
**Blue**: False positive  
**White**: True negative    
**Green**: False negative  

#### Result of EMD-2984 slice, manual marking
![emd-2984-signal-noise](https://github.com/LesikDee/ED_Denoising/blob/master/results/emd2984.png)  

#### Result of EMD-6479 slice, manual marking
![emd-6479-signal-noise](https://github.com/LesikDee/ED_Denoising/blob/master/results/emd6479.png)  

### Metrics indicators for EMD-2984
![emd-6479-metrics-indicators](https://github.com/LesikDee/ED_Denoising/blob/master/results/metrics.png)  