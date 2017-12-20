import pycrystem as pc
import numpy as np

folder = '/home/pc494/Documents/data/pattern_matching_in_perovskites/'

dp = pc.load(folder+'QD-03.blo')
dp = dp.inav[100:102,100:102]
dp.apply_affine_transformation(D = np.array([[0.99, 0.00, 0.00],
                                             [0.00, 0.69, 0.00],
                                             [0.00, 0.00, 1.00]]),show_progressbar=False)
dp.set_calibration(0.032)

