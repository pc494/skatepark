### Binning signals.
import pyxem as pxm

for n in ['02','03','04','05','06','07','08','09','10','11']:
    dp = pxm.load('/home/pc494/Documents/data/cBN/160401_MultipleZoneAxes/160401_'+n+'.blo')
    dp = dp.rebin(scale=[1,1,4,4])
    dp.save('binned'+n+'.hspy')
    
    
###