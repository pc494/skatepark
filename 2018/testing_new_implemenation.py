import numpy as np
import pyxem as pxm
import pymatgen as pmg

dp = pxm.load('/home/phillip/Documents/code/phd/data/QD-03.blo')
rot_array = np.loadtxt('/home/phillip/Documents/code/phd/data/mmm_grid_euler.bin')
structure = pmg.Structure.from_file("/home/phillip/Documents/code/phd/data/CsPbBr3_1.cif")

dp1   = dp.inav[0,0]

rot_list = rot_array.tolist()
rot_list = rot_list[0:1]
edc = pxm.DiffractionGenerator(300, 0.025)
diff_gen = pxm.DiffractionLibraryGenerator(edc)
struc_lib = dict()
struc_lib["CsPbBr3"] = (structure, rot_list)
library = diff_gen.get_diffraction_library(struc_lib,
                                            calibration=1.2/128,
                                            reciprocal_radius=0.65,
                                            representation='euler',
                                            half_shape = (72,72)
                                            )

single_element = library['CsPbBr3'][(1.047198,0.043633,3.665191)]

from pyxem.utils import correlate
import time 

start = time.time()
for i in [1]*500:
    correlate(dp1.data,single_element)
end = time.time()
print(end-start)