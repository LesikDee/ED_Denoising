import numpy as np
import dsn6_parser
import noise_signal_plot
from molecule import MolRepresentation


class Model:
    def __init__(self, ed_2fo_fc, ed_fo_fc):
        self.ed_2fo_fc = ed_2fo_fc
        self.ed_fo_fc = ed_fo_fc

        self.ed_fc = MolRepresentation()    # calculated ed
        self.ed_fo = MolRepresentation()    # obs ed

    def execute(self):
        self.ed_fc.header = self.ed_2fo_fc.header
        self.ed_fo.header = self.ed_2fo_fc.header

        n = len(self.ed_2fo_fc.data)
        fo_data_buffer = np.empty(n, 'f4')
        for i in range(n):
            fo_data_buffer[i] = self.ed_2fo_fc.data[i] - self.ed_fo_fc.data[i]

        self.ed_fo.data = fo_data_buffer


if __name__ == '__main__':
    file_2fo_fc = '../mol_data/dsn6/4nre_2fofc.dsn6'
    file_fo_fc = '../mol_data/dsn6/4nre_fofc.dsn6'

    ed_2fo_fc = dsn6_parser.read(file_2fo_fc)
    ed_fo_fc = dsn6_parser.read(file_fo_fc)

    model = Model(ed_2fo_fc, ed_fo_fc)
    model.execute()
    model.ed_fo.stats_calc()
    noise_signal_plot.build_graph(model.ed_fo)



