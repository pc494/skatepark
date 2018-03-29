import pyxem as pxm
import pymatgen as pmg
import numpy as np
from pyxem.generators.indexation_generator import IndexationGenerator
from pyxem.utils.plot import generate_marker_inputs_from_peaks
from pyxem.utils.sim_utils import peaks_from_best_template
import hyperspy.api as hs
import pickle
from pyxem.utils.orientation_utils import *
from pyxem.utils.orientation_utils import _sting_ray

theoretical_distance = 1/np.sqrt((3.615**2)/(8))
pixel_distance = 79.6/4 # np.sqrt(50**2 + 61.7**2)

a = 3.615
B = pmg.Element("B")
N = pmg.Element("N")
lattice = pmg.Lattice.cubic(a)
structure = pmg.Structure.from_spacegroup("F-43m",lattice, [B,N], [[0, 0, 0],[0.25,0.25,0.25]])

with open('c-BN-5deg.pickle', 'rb') as handle:
    library = pickle.load(handle)

if True:
    
    half_side_length = (512/8)
    edc = pxm.DiffractionGenerator(300, 5e-2)
    diff_gen = pxm.DiffractionLibraryGenerator(edc)
    rot_list = build_linear_grid_in_euler(0,20-2,35-2,4,0.4)
    struc_lib = dict()
    struc_lib["A"] = (structure,rot_list)


    library = diff_gen.get_diffraction_library(struc_lib,
                                           calibration=theoretical_distance/pixel_distance,
                                           reciprocal_radius=1.5,
                                           half_shape=(half_side_length,half_side_length),
                                           representation='euler',
                                           with_direct_beam=False)

    with open('c-BN-0.4deg_x.pickle', 'wb') as handle:
        pickle.dump(library, handle, protocol=pickle.HIGHEST_PROTOCOL)

match_results_list = []
for x in [0,25,50,75,100,125,150,175,200]:
    for y in [0,25,50,75,100,125,150]:
        s = hs.load('data/binned02.hspy',lazy=True)
        s = s.inav[x:x+25,y:y+25]
        s.compute() #unlazy
        dp = pxm.ElectronDiffraction(s)
        dp.apply_affine_transformation(_sting_ray)
        centers = dp.get_direct_beam_position(method='blur',sigma=3,progress_bar=False) #checking centers, also BUG!
        shifts = centers.data - np.array([64,64])
        shifts = shifts.reshape(625,2)
        dp.align2D(shifts=shifts, crop=False, fill_value=0)
        dp.set_diffraction_calibration(theoretical_distance/pixel_distance)
        ## Calibrate then do the main component

        indexer = IndexationGenerator(dp,library)
        match_results = indexer.correlate()
        match_results_list.append(match_results.data)
        with open('MRlist.pickle', 'wb') as handle:
            pickle.dump(match_results_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(str(x)+' and ' + str(y))
        peaks = match_results.map(peaks_from_best_template,phase=["A"],library=library,inplace=False)
        mmx,mmy = generate_marker_inputs_from_peaks(peaks)
        s.plot(cmap='viridis')
        for mx,my in zip(mmx,mmy):
            m = hs.markers.point(x=mx,y=my,color='red',marker='x') #see visual test
            s.add_marker(m,plot_marker=True,permanent=False)
        #raise KeyboardInterrupt