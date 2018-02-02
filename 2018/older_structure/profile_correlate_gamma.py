import numpy as np
import pycrystem as pxm

dp = pxm.load('/home/phillip/Documents/code/phd/data/QD-03.blo')
rot_array = np.loadtxt('/home/phillip/Documents/code/phd/data/mmm_grid_euler.bin')
structure = pxm.Structure.from_file("/home/phillip/Documents/code/phd/data/CsPbBr3_1.cif")

dp1   = dp.inav[0,0]
dp1np = dp.inav[0,0].data

rot_list = rot_array.tolist()
rot_list = rot_list[0:1]
edc = pxm.ElectronDiffractionCalculator(300, 0.025)
diff_gen = pxm.DiffractionLibraryGenerator(edc)
struc_lib = dict()
struc_lib["CsPbBr3"] = (structure, rot_list)
library = diff_gen.get_diffraction_library(struc_lib,
                                            calibration=1.2/128,
                                            reciprocal_radius=0.65,
                                            representation='euler')

dp2 = library['CsPbBr3'][(1.047198,0.043633,3.665191)]


def access_dict():
    return library['CsPbBr3'][(1.047198,0.043633,3.665191)]

def access_element():
    return dp2.coordinates

import timeit
alpha = timeit.timeit(access_dict,number=int(1e5))
beta = timeit.timeit(access_element,number=int(1e5))
