import numpy as np
import math
import os
from scripts.molecule import MolRepresentation

hD = {  # header Description
    "XStart": 0,
    "YStart": 1,
    "ZStart": 2,
    "NC": 3,   # XExtent
    "NR": 4,   # YExtent
    "NS": 5,   # ZExtent
    "XSP": 6,  # Sampling rate
    "YSP": 7,
    "ZSP": 8,
    "ACE": 9,  # A Cell Edge
    "BCE": 10,
    "CCE": 11,
    "Alpha": 12,
    "Beta": 13,
    "Gamma": 14,
    "div": 15,
    "sum": 16,
    "SF": 17,  # Cell Constant Scaling Factor
    "C100": 18,  # for checking endian
}


class DSN6Header:
    def __init__(self, buffer):
        self.fields = {}
        self.need_revert = False
        data16int = np.array(np.frombuffer(buffer, 'i2'), 'i2')

        for val in hD:
            self.fields[val] = data16int[hD[val]]

        if self.fields['C100'] != 100:
            for i in range(256):
                val = data16int[i]
                data16int[i] = ((val & 0xff) << 8) | ((val >> 8) & 0xff)

            for val in hD:
                self.fields[val] = data16int[hD[val]]

            self.need_revert = True

        if self.fields['C100'] != 100:
            raise SyntaxError

        self.fields["ACE"] /= self.fields["SF"]
        self.fields["BCE"] /= self.fields["SF"]
        self.fields["CCE"] /= self.fields["SF"]

        self.fields["Alpha"] = self.fields["Alpha"] * 180.0 / math.pi / self.fields["SF"]
        self.fields["Beta"] = self.fields["Beta"] * 180.0 / math.pi / self.fields["SF"]
        self.fields["Gamma"] = self.fields["Gamma"] * 180.0 / math.pi / self.fields["SF"]

        self.fields["div"] /= 100

        self.nsec = self.fields["ZStart"]


class DSN6File(MolRepresentation):
    def __init__(self, name, header: DSN6Header, data):
        super().__init__(name)

        self.header = header

        byte_data = np.array(np.frombuffer(data, 'u1'), 'u1')
        if header.need_revert:
            for i in range(len(byte_data) // 2):
                tmp = byte_data[2 * i]
                byte_data[2 * i] = byte_data[2 * i + 1]
                byte_data[2 * i + 1] = tmp


        x_extent, y_extent, z_extent = int(header.fields["NC"]), \
                                       int(header.fields["NR"]), int(header.fields["NS"])

        div, addendum = int(header.fields["div"]), int(header.fields["sum"])
        buffer = np.empty(x_extent * y_extent * z_extent, 'f4')

        offset = 0
        x_blocks = int(math.ceil(x_extent / 8))
        y_blocks = int(math.ceil(y_extent / 8))
        z_blocks = int(math.ceil(z_extent / 8))

        for z_block in range(z_blocks):
            for y_block in range(y_blocks):
                for x_block in range(x_blocks):
                    i = 0
                    while i < 512:
                        x = i % 8 + 8 * x_block
                        y = (i % 64) // 8 + 8 * y_block
                        z = i // 64 + 8 * z_block

                        if x < x_extent and y < y_extent and z < z_extent:
                            current_cell_ind = ((z * y_extent) + y) * x_extent + x
                            buffer[current_cell_ind] = (int(byte_data[offset]) - addendum) / div
                            offset += 1
                            i += 1
                        else:
                            offset += 8 - i % 8
                            i += 8 - i % 8

        self.values = np.ndarray((z_extent, y_extent, x_extent), 'f4',  buffer=buffer)
        self.buffer = buffer

def read(filename):
    with open(filename, 'rb') as f:
        header = DSN6Header(f.read())
        f.seek(512)
        data = f.read()
        return DSN6File(os.path.basename(filename), header, data)
