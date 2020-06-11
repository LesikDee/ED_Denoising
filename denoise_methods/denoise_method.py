import numpy as np
class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Voxel:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class DenoiseMethod:
    def __init__(self, data: np.ndarray):
        self. data = data

        self.length = len(data)
        self.height = len(data[0])
        self.width = len(data[0][0])

    def execute_2d(self):
        pass

    def execute_3d(self):
        pass

