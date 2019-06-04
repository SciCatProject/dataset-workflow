from __future__ import (absolute_import, division, print_function)
from mantid.simpleapi import *
from ISISCommandInterface import *


class SANS2DLimitEventsTime(object):

    def __init__(self, input_data):
        self.input_data = input_data

    def run(self):
        SANS2D()
        MaskFile('/data/MaskSANS2DReductionGUI_LimitEventsTime.txt')
        AssignSample('/data/SANS2D00022048.nxs')
        return WavRangeReduction()


def main(input_data):
    sans2d = SANS2DLimitEventsTime(input_data)
    reduce_data = sans2d.run()
    return {"data": reduce_data}
