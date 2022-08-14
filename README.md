# Electron density denoising algorithms implementation 
Implementation of noise reduction algorithms applying to electron density maps. This code is part of my [master's qualification diploma](https://elib.spbstu.ru/dl/3/2020/vr/vr20-1604.pdf/en/info).

#### Example of current implementation BM4D denoise algorithm applying to [EMD-2984 map](https://www.ebi.ac.uk/emdb/EMD-2984) visualized through [miew visualizer](https://miew.opensource.epam.com/).
![Miew – 3D Molecular Viewer - Google Chrome 2022-08-14 23-52-43_Segment_0_gif_008](https://user-images.githubusercontent.com/22669290/184553404-890da389-0adb-4dd1-9914-2c5e9c3e7aa5.gif)
![Miew – 3D Molecular Viewer - Google Chrome 2022-08-15 00-09-23_Segment_0_gif_003](https://user-images.githubusercontent.com/22669290/184553710-2a7382c4-0fbf-443e-817d-8df28a11c41e.gif)  
The left picture is the origin EMD-2984 map and the right picture is denoised by [current BM4D algorithm](https://github.com/LesikDee/ED_Denoising/blob/master/denoise_methods/BM4D.py) map. 

