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

@profile
def correlate_danger_1(image, pattern,arg3):
    shape = image.shape
    half_shape = tuple(i // 2 for i in shape)
    mask = np.abs(pattern.coordinates[:,2]) < 1e-2
    pixel_coordinates = np.rint(pattern.calibrated_coordinates[:,:2]+half_shape).astype(int)
    image_intensities = image[pixel_coordinates[:, 0][mask], pixel_coordinates[:, 1][mask]]
    pattern_intensities = pattern.intensities[mask]
    return np.dot(image_intensities,pattern_intensities)/np.sqrt(np.dot(pattern_intensities,pattern_intensities))

@profile
def correlate_danger_2(image, pattern,half_shape):
    mask = np.abs(pattern.coordinates[:,2]) < 1e-2
    pattern_intensities = pattern.intensities[mask]
    pixel_coordinates = np.rint(pattern.calibrated_coordinates[:,:2]+half_shape).astype(int)
    image_intensities = image[pixel_coordinates[:, 0][mask], pixel_coordinates[:, 1][mask]]
    return np.dot(image_intensities,pattern_intensities)/np.sqrt(np.dot(pattern_intensities,pattern_intensities))

for i in [1]*500:
    safer_alpha = correlate_danger_1(dp1np,dp2,None)
    danger_alpha = correlate_danger_2(dp1np,dp2,(72,72))

def wrapper(function):
    def wrapped():
        return function(dp1np,dp2,(72,72))
    return wrapped

wrapped_1 = wrapper(correlate_danger_1)
wrapped_2 = wrapper(correlate_danger_2)

if False:
    import timeit
    alpha = timeit.timeit(wrapped_1,number=int(1e5))
    beta = timeit.timeit(wrapped_2,number=int(1e5))
