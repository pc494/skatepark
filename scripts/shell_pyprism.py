#!/usr/bin/env python3

""" 
Usage:
     shell_pyprism.py <alpha_divider> <probe_divider> <x_size> <z_size>
"""

from docopt import docopt
args = docopt(__doc__)
alpha_divider = float(args["<alpha_divider>"]) 
probe_divider = float(args["<probe_divider>"]) 
xy_size = float(args["<x_size>"])
z_size  = float(args["<z_size>"])



import pyxem as pxm
import pymatgen as pmg
from matplotlib import pyplot as plt
import numpy as np
from pyxem.utils.pyprismatic_io_utils import *
import pyprismatic as pr
import os

try:
    os.remove('PP_input.XYZ')
except FileNotFoundError:
    pass

Ga = pmg.Element("Ga")
As = pmg.Element("As")
lattice = pmg.Lattice.cubic(5.65)

structure = pmg.Structure.from_spacegroup("F-43m",lattice, [Ga,As], [[0, 0, 0],[0.5,0.5,0.5]])


structure.make_supercell([xy_size,xy_size,z_size])
ediff = pxm.ElectronDiffractionCalculator(200., 0.025)

meta_params = {}
alpha_divider = 3
probe_divider = 2
meta_params['save4DOutput'] = True
meta_params['save3DOutput'] = False
meta_params['scanWindowXMin'] = 0.495
meta_params['scanWindowXMax'] = 0.515
meta_params['scanWindowYMin'] = 0.495
meta_params['scanWindowYMax'] = 0.515
meta_params['alphaBeamMax'] = 0.024/alpha_divider
meta_params['probeSemiangle'] = 0.02/probe_divider
meta_params['tileX']=1
meta_params['tileY']=1
meta_params['realspacePixelSizeX']=0.1
meta_params['realspacePixelSizeY']=0.1

diff_dat_m = ediff.calculate_ed_data_dynamic(structure,delete_mode=False,prismatic_kwargs=meta_params)

dp = pxm.ElectronDiffraction(np.divide(diff_dat_m,np.max(diff_dat_m)))
plt.figure()
plt.imshow(dp.inav[0,0],cmap='viridis')
plt.draw()
plt.savefig('image.png')




