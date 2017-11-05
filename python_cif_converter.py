""" Converting an inspected cif file into .xyz format a la PyPrismatic"""

import numpy as np

file = open('azif_hacked.cif', 'r+')
info = file.readlines()
lines = []
for line in info:
   lines.append(line)

## Cut top 6 lines of dullness
lines = lines[6:]

cleaner_lines = []

def clean(line):
    while '' in line:
        line.remove('')
    return line 

for line in lines:
    cleaner_lines.append(clean(line.split(' ')))

species = []
x,y,z = [],[],[]

for line in cleaner_lines[:-1]: #avoid the trail line
    # TODO zip this up
    x.append(line[2])
    y.append(line[3])
    z.append(line[4][:-2]) #drops the newline character
    species.append(line[1])

# Convert Species to Atomic Number
species_dict = {'D':1, 'C':6, 'N':7, 'Zn':30}
atomic_numbers = []

for atom in species:
    atomic_numbers.append(species_dict[atom])


atomic_numbers = np.asarray(atomic_numbers)
x = np.asarray(x,dtype=float)*49.38898 #cell dimensions from the full .cif file, this turns fractional to atomic co-ords
y = np.asarray(y,dtype=float)*49.38898 #as above
z = np.asarray(z,dtype=float)*49.38898

line_2 = [np.max(x),np.max(y),np.max(z)]
    
debeye_waller = 1*np.ones_like(atomic_numbers)
percent_occupied = 1*np.ones_like(atomic_numbers)
        
printing_array = np.vstack(([[atomic_numbers],[x],[y],[z],[percent_occupied],[debeye_waller]]))
        
with open('PP_input.XYZ', 'a') as f:
     print("Default Comment",file=f)
     print('    {0:.3g}   {1:.3g}   {2:.3g}'.format(line_2[0],line_2[1],line_2[2]),file=f)
     for row in printing_array.T:
         print('{0:.3g} {1:.4f} {2:.4f} {3:.4f} {4:.3f} {5:.3f}'.format(
               row[0],row[1],row[2],row[3],row[4],row[5]),
               file=f)
     print("-1",file=f)
  
