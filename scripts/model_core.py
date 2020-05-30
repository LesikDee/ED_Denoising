import numpy as np
from scripts.molecule import MolRepresentation
import copy

class Model:
    def __init__(self, ed_2fo_fc: MolRepresentation, ed_fo_fc: MolRepresentation):
        self.ed_2fo_fc = ed_2fo_fc
        self.ed_fo_fc = ed_fo_fc

        self.ed_fc = MolRepresentation(ed_2fo_fc.name)    # calculated ed
        self.ed_fo = MolRepresentation(ed_2fo_fc.name)    # observed ed

        self.ed_fc.header = copy.deepcopy(self.ed_2fo_fc.header)
        self.ed_fo.header = copy.deepcopy(self.ed_2fo_fc.header)

    def execute_fo(self):
        n = len(self.ed_2fo_fc.buffer)
        fo_data_buffer = np.empty(n, 'f4')
        for i in range(n):
            fo_data_buffer[i] = self.ed_2fo_fc.buffer[i] - self.ed_fo_fc.buffer[i]

        self.ed_fo.buffer = fo_data_buffer
        self.ed_fo.update_buffer(self.ed_fo.buffer)

    def execute_fc(self):
        n = len(self.ed_2fo_fc.buffer)
        fc_data_buffer = np.empty(n, 'f4')
        for i in range(n):
            fc_data_buffer[i] = self.ed_2fo_fc.buffer[i] - 2 * self.ed_fo_fc.buffer[i]

        self.ed_fc.buffer = fc_data_buffer
        self.ed_fc.update_buffer(self.ed_fc.buffer)