import numpy as np


class Model:
    ed_fc = {}  # calculated ed
    ed_fo = {}  # obs ed

    def __init__(self, ed_2fc_fo, ed_fc_fo):
        self.ed_2fc_fo = ed_2fc_fo
        self.ed_fc_fo = ed_fc_fo

    def execute(self):
        self.ed_fc.header = self.ed_2fc_fo.header
        self.ed_fo.header = self.ed_2fc_fo.header

        n = len(self.ed_2fc_fo.data)
        fo_data_buffer = np.empty(n, 'f4')
        for i in range(n):
            fo_data_buffer[i] = self.ed_2fc_fo.data[i] - self.ed_fc_fo.data[i]


if __name__ == '__main__':
    pass
