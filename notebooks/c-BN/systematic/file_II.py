import pyxem as pxm
import pymatgen as pmg
import numpy as np
from pyxem.generators.indexation_generator import IndexationGenerator
from pyxem.utils.plot import generate_marker_inputs_from_peaks
from pyxem.utils.sim_utils import peaks_from_best_template
import hyperspy.api as hs
import pickle

def build_structure_lib(structure,rot_list):
    struc_lib = dict()
    struc_lib["A"] = (structure,rot_list)
    return struc_lib    

def build_linear_grid_in_euler(alpha_min,alpha_max,beta_min,beta_max,gamma_min,gamma_max,resolution):
    a = np.arange(alpha_min,alpha_max,step=resolution)
    b = np.arange(beta_min,beta_max,step=resolution)
    c = np.arange(gamma_min,gamma_max,step=resolution)
    from itertools import product
    return list(product(a,b,c))

def get_WZL_axis(library,phase,angle):
    indicies = library[phase][angle]['Sim'].indices
    for U in [0,1,2,3,-3,-2,-1]:
        for V in [0,1,2,3,-3,-2,-1]:
            for W in [1,2,3,-3,-2,-1]:
                direction = np.array([U,V,W])
                if np.all(np.dot(indicies,direction) == 0):
                    return direction
    print("No direction found")
    return 0


theoretical_distance = 1/np.sqrt((3.615**2)/(8))
a = 3.615
B = pmg.Element("B")
N = pmg.Element("N")
lattice = pmg.Lattice.cubic(a)
structure = pmg.Structure.from_spacegroup("F-43m",lattice, [B,N], [[0, 0, 0],[0.25,0.25,0.25]])

if True:
    dp = pxm.ElectronDiffraction(pxm.load('data/binned02.hspy'))
    #dp.plot()
    #raise KeyboardInterrupt
    ## get an undeformed section

    dp = pxm.ElectronDiffraction(dp.inav[0:4,104:108])

    """
    ## get a deformed section
    dp = pxm.ElectronDiffraction(sample.inav[110:150,25:65])
    dp = pxm.ElectronDiffraction(sample.inav[116:143,19:46])
    """

    #CORRECTING FOR CAMERA
    dp.apply_affine_transformation(np.array([[0.99,0,0],
                                             [0,0.69,0],
                                             [0,0,1]]))
    #CORRECTING FOR BEING OFF CENTER
    #cents = dp.get_direct_beam_position(method='blur',sigma=10,progress_bar=False) #checking centers, also BUG!
    dp.apply_affine_transformation(D=np.array([[1,0,0],
                                               [0,1,0.75],
                                               [0,0,1]]))

pixel_distance = 79.6/4 # np.sqrt(50**2 + 61.7**2)
dp.set_calibration(theoretical_distance/pixel_distance)
#dp.set_calibration(theoretical_distance/pixel_distance)
## Calibrate then do the main component

if True:
    
    half_side_length = (512/8)
    edc = pxm.DiffractionGenerator(300, 5e-2)
    diff_gen = pxm.DiffractionLibraryGenerator(edc)
    rot_list = build_linear_grid_in_euler(25,35,125,135,30,40,1)
    struc_lib = build_structure_lib(structure,rot_list)


    library = diff_gen.get_diffraction_library(struc_lib,
                                           calibration=theoretical_distance/pixel_distance,
                                           reciprocal_radius=1,
                                           half_shape=(half_side_length,half_side_length),
                                           representation='euler',
                                           with_direct_beam=False)

    with open('c-BN-1deg_x.pickle', 'wb') as handle:
        pickle.dump(library, handle, protocol=pickle.HIGHEST_PROTOCOL)

if False:
    with open('c-BN-5deg.pickle', 'rb') as handle:
        library = pickle.load(handle)

indexer = IndexationGenerator(dp,library)
match_results = indexer.correlate()

# good start is 25, 175, 40
print(match_results.isig[1:4,0].data)

peaks = match_results.map(peaks_from_best_template,phase=["A"],library=library,inplace=False)
mmx,mmy = generate_marker_inputs_from_peaks(peaks)
dp.plot(cmap='viridis')
for mx,my in zip(mmx,mmy):
    m = hs.markers.point(x=mx,y=my,color='red',marker='x') #see visual test
    dp.add_marker(m,plot_marker=True,permanent=False)