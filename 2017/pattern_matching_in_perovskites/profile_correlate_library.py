""" Script to profile, ignore the nonesense import count"""

import warnings
warnings.filterwarnings('once') #only get the hyperspy load warning once
import pycrystem as pc
import numpy as np
import hyperspy.api as hs
from matplotlib import pyplot as plt
from pycrystem.indexation_generator import *
from pycrystem.utils.expt_utils import *
from pycrystem import ElectronDiffraction
from pycrystem.indexation_generator import IndexationGenerator
from load_data import dp
from generate_library import structure,rot_list,edc,diff_gen,struc_lib
from hyperspy.signals import BaseSignal
from heapq import nlargest
from operator import itemgetter
from pycrystem.utils import correlate,_correlate
from pycrystem.crystallographic_map import CrystallographicMap

library = diff_gen.get_diffraction_library(struc_lib,
                                            calibration=1.2/128,
                                            reciprocal_radius=1.,
                                            representation='euler')

image = dp.inav[0,0].data

@profile
def correlate_library(image, library, n_largest):
    """Correlates all simulated diffraction templates in a DiffractionLibrary
    with a particular experimental diffraction pattern (image) stored as a
    numpy array.
    """
    i=0
    out_arr = np.zeros((n_largest * len(library),5))
    for key in library.keys():
        if n_largest:
            pass
        else:
            n_largest=len(library[key])
        correlations = dict()
        for orientation, diffraction_pattern in library[key].items():
            correlation = correlate(image, diffraction_pattern)
            correlations[orientation] = correlation
        res = nlargest(n_largest, correlations.items(), key=itemgetter(1))
        for j in np.arange(n_largest):
            out_arr[j + i*n_largest][0] = i
            out_arr[j + i*n_largest][1] = res[j][0][0]
            out_arr[j + i*n_largest][2] = res[j][0][1]
            out_arr[j + i*n_largest][3] = res[j][0][2]
            out_arr[j + i*n_largest][4] = res[j][1]
        i = i + 1
        return out_arr
    
sol = correlate_library(image,library,1)