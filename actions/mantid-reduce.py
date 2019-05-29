from __future__ import (absolute_import, division, print_function)
from mantid.simpleapi import *
from ISISCommandInterface import *


class SANS2DLimitEventsTime:

    def __init__(self, input_data):
        self.input_data = input_data

    def runTest(self):
        SANS2D()
        MaskFile('/data/MaskSANS2DReductionGUI_LimitEventsTime.txt')
        AssignSample('/data/SANS2D00022048.nxs')
        WavRangeReduction()

    def validate(self):
        self.disableChecking.append('SpectraMap')
        self.disableChecking.append('Axes')
        self.disableChecking.append('Instrument')
        return {'a': '22048rear_1D_1.5_12.5', 'b': 'SANSReductionGUI_LimitEventsTime.nxs'}


def main(input_data):
    sans2d = SANS2DLimitEventsTime(input_data)
    sans2d.runTest()
    return sans2d.validate()
