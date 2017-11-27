import hyperspy.api as hs
from matplotlib import pyplot as plt
import numpy as np
import pycrystem as pc
plt.rcParams['image.cmap'] = 'gray'

dp = pc.load("/home/pc494/Documents/data/GaN_intro/GaN_indent.blo")

dp = dp.inav[0:25,475:500]
dp.apply_affine_transformation(np.array([[0.99,0,0],
                                         [0,0.69,0],
                                         [0,0,1]]));
peaks = dp.find_peaks('max')

if dp.axes_manager.signal_shape[0] == dp.axes_manager.signal_shape[1]:
    peaks.data = peaks.data + (dp.axes_manager.signal_shape[0])/2 * 0.0076034063260340635
else:
    raise NotImplementedError('Needs a square signal')
    
def find_max_length_peaks(peaks):
    x_size,y_size = peaks.axes_manager.navigation_shape[0],peaks.axes_manager.navigation_shape[1]
    length_of_longest_peaks_list = 0
    for x in np.arange(0,x_size):
            for y in np.arange(0,y_size):
                if peaks.data[x,y].shape[0] > length_of_longest_peaks_list:
                    length_of_longest_peaks_list = peaks.data[x,y].shape[0]
    return length_of_longest_peaks_list  


@profile
def generate_markers_from_peaks(peaks):
    markx,marky = [],[]
    x_size,y_size = peaks.axes_manager.navigation_shape[0],peaks.axes_manager.navigation_shape[1]
    max_peak_count = find_max_length_peaks(peaks)
    for k in np.arange(0,max_peak_count):
        mx,my = np.empty([x_size,y_size]),np.empty([x_size,y_size])
        for x in np.arange(0,x_size):
            for y in np.arange(0,y_size):
                try:
                    mx[x,y] = peaks.inav[x,y].data[k][1]
                    my[x,y] = peaks.inav[x,y].data[k][0]
                except IndexError: #we have fewer than 'max_peak_count' peaks, so no marker
                    mx[x,y] = (np.nan)
                    my[x,y] = (np.nan)
        markx.append(mx.T)
        marky.append(my.T)
    
    return markx,marky 

markx,marky = generate_markers_from_peaks(peaks)
