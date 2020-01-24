import numpy as np
import dsn6_parser
import noise_signal_plot


class MolRepresentation:
    def __init__(self):
        self.header: {}
        self.data: np.ndarray


class Model:
    # ed_fc = {}  # calculated ed
    # ed_fo = {}  # obs ed

    def __init__(self, ed_2fo_fc, ed_fo_fc):
        self.ed_2fo_fc = ed_2fo_fc
        self.ed_fo_fc = ed_fo_fc

        self.ed_fc = MolRepresentation()
        self.ed_fo = MolRepresentation()

    def execute(self):
        self.ed_fc.header = self.ed_2fo_fc.header
        self.ed_fo.header = self.ed_2fo_fc.header

        n = len(self.ed_2fo_fc.data)
        fo_data_buffer = np.empty(n, 'f4')
        for i in range(n):
            fo_data_buffer[i] = self.ed_2fo_fc.data[i] - self.ed_fo_fc.data[i]

        self.ed_fo.data = fo_data_buffer


if __name__ == '__main__':
    file_2fo_fc = '../mol_data/dsn6/4xn6_2fofc.dsn6'
    file_fo_fc = '../mol_data/dsn6/4xn6_fofc.dsn6'

    ed_2fo_fc = dsn6_parser.read(file_2fo_fc)
    ed_fo_fc = dsn6_parser.read(file_fo_fc)

    model = Model(ed_2fo_fc, ed_fo_fc)
    model.execute()
    noise_signal_plot.build_graph(model.ed_fo)

