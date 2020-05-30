import numpy as np

a1 = np.zeros([5,5])
a2 = np.zeros([3,3])
a2 += 1
a1[1:4, 1:4] = a2
print(a1)

