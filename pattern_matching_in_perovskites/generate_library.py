import pycrystem as pc
import numpy as np

folder = '/home/pc494/Documents/data/pattern_matching_in_perovskites/'

structure = pc.Structure.from_file(folder+"CsPbBr3_1.cif")
rot_array = np.loadtxt(folder + 'mmm_grid_euler.bin')
rot_list = rot_array.tolist()[::5] #taking every 5th rotation option
edc = pc.ElectronDiffractionCalculator(300, 0.025)
diff_gen = pc.DiffractionLibraryGenerator(edc)
struc_lib = dict()
struc_lib["CsPbBr3"] = (structure, rot_list)

