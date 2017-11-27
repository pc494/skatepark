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
    mark = []
    x_size,y_size = peaks.axes_manager.navigation_shape[0],peaks.axes_manager.navigation_shape[1]
    max_peak_count = find_max_length_peaks(peaks)
    for k in np.arange(0,max_peak_count):
        m = np.empty([x_size,y_size,2])
        for x in np.arange(0,x_size):
            for y in np.arange(0,y_size):
                try:
                    m[x,y] = peaks.inav[x,y].data[k]   
                except IndexError: #we have fewer than 'max_peak_count' peaks, so no marker
                    m[x,y,0] = np.nan
                    m[x,y,1] = np.nan
        mark.append(m.T)
        
    return mark

mark = generate_markers_from_peaks(peaks)
