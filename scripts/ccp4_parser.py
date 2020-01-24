import numpy as np
import os

hD = {  # header Description
    "NC": [0, 'u4'],
    "NR": [1, 'u4'],
    "NS": [2, 'u4'],
    "MODE": [3, 'u4'],
    "NCSTART": [4, 'i4'],
    "NRSTART": [5, 'i4'],
    "NSSTART": [6, 'i4'],
    "NX": [7, 'u4'],
    "NY": [8, 'u4'],
    "NZ": [9, 'u4'],
    "XlengthCell": [10, 'f4'],
    "YlengthCell": [11, 'f4'],
    "ZlengthCell": [12, 'f4'],
    "alpha": [13, 'f4'],
    "beta": [14, 'f4'],
    "gamma": [15, 'f4'],
    "mapc": [16, 'f4'],
    "mapr": [17, 'f4'],
    "maps": [18, 'f4'],
    "amin": [19, 'f4'],
    "amax": [20, 'f4'],
    "amean": [21, 'f4'],
    "ispg": [22, 'u4'],
    "nsymbt": [23, 'u4'],
    "originX": [34, 'f4'],
    "originY": [35, 'f4'],
    "originZ": [36, 'f4'],
    "map": [52, 'f4'],
    "machine": [53, 'f4'],
    "sd": [54, 'f4'],
    "nlabel": [55, 'f4'],
    "label": [56, 'f4']
}


# http://www.ccp4.ac.uk/html/maplib.html
class CCP4Header:
    def __init__(self, buffer):
        self.fields = {}
        data32int = np.frombuffer(buffer, 'i4')
        data32uint = np.frombuffer(buffer, 'u4')
        data32float = np.frombuffer(buffer, 'f4')

        data_dict = {
            'f4': data32float,
            'u4': data32uint,
            'i4': data32int
        }
        for val in hD:
            self.fields[val] = data_dict[hD[val][1]][hD[val][0]]

        self.data_size = self.fields["NC"] * self.fields["NR"] * self.fields["NS"]
        self.mean = self.fields["amean"]
        self.stddev = self.fields["sd"]
        self.nsec = self.fields["NS"]


class CCP4File:
    def __init__(self, name, header, data):
        self.name = name
        self.header = header
        self.data = np.array(np.frombuffer(data, 'f4'), 'f4')

        self.values = np.ndarray((header.fields["NS"], header.fields["NR"], header.fields["NC"]), 'f4',
                                 buffer=self.data)


def read(filename):
    with open(filename, 'rb') as f:
        header = CCP4Header(f.read(1024))
        f.seek(1024 + header.fields["nsymbt"])
        data = f.read()
        return CCP4File(os.path.basename(filename), header, data)
