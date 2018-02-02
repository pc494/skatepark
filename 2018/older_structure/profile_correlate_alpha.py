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
def correlate_danger(image, pattern,
              include_direct_beam=False,
              sim_threshold=1e-5,
              interpolate=False,
              **kwargs):
    shape = image.shape
    half_shape = tuple(i // 2 for i in shape)
    mask = np.abs(pattern.coordinates[:,2]) < 1e-2
    pixel_coordinates = np.rint(pattern.calibrated_coordinates[:,:2]+half_shape).astype(int)
    image_intensities = image[pixel_coordinates[:, 0][mask], pixel_coordinates[:, 1][mask]]
    pattern_intensities = pattern.intensities[mask]
    return np.dot(image_intensities,pattern_intensities)/np.sqrt(np.dot(pattern_intensities,pattern_intensities))

@profile
def correlate_safer(image, pattern,
              include_direct_beam=False,
              sim_threshold=1e-5,
              interpolate=False,
              **kwargs):
    shape = image.shape
    half_shape = tuple(i // 2 for i in shape)
    in_bounds_z = np.abs(pattern.coordinates[:,2]) < 1e-2
    
    pixel_coordinates = np.rint(pattern.calibrated_coordinates[:,:2]+half_shape).astype(int)
    in_bounds = np.product((pixel_coordinates > 0)*(pixel_coordinates < shape[0]), axis=1)

    pattern_intensities = pattern.intensities
    large_intensities = pattern_intensities > sim_threshold
    mask = np.logical_and(in_bounds_z,np.logical_and(in_bounds, large_intensities))
    image_intensities = image[pixel_coordinates[:, 0][mask], pixel_coordinates[:, 1][mask]]
    
    pattern_intensities = pattern_intensities[mask]
    numerator = np.dot(image_intensities,pattern_intensities)
    denominator = np.sqrt(np.dot(pattern_intensities,pattern_intensities)*np.sum(np.dot(image,image)))
    
    return np.nan_to_num(numerator/denominator)

safer_alpha = correlate_safer(dp1np,dp2)
danger_alpha = correlate_danger(dp1np,dp2)

##results are equivilant (danger leaves out a factor as a design feature)
