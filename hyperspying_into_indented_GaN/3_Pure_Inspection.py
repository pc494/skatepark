import hyperspy.api as hs
import numpy as np
import pycrystem as pc
from matplotlib import pyplot as plt

dp = pc.load("/home/pc494/Documents/data/GaN_intro/GaN_indent.blo")
dp = dp.inav[0:100,450:500]
dp.apply_affine_transformation(np.array([[0.99,0,0],
                                         [0,0.69,0],
                                         [0,0,1]]));


peak_finder = pc.utils.peakfinders2D.find_peaks_max
peak = dp.map(peak_finder,inplace=False)
dp.plot(cmap='viridis')
plt.show()