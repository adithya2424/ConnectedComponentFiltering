import nrrd
import matplotlib.pyplot as plt
import numpy as np
from displayvol import *
from surface_adi_new import *
from mayavi import mlab
import pygame
import seaborn as sb
import pandas as pd


# load a CT image to play with
img, imgh = nrrd.read(
    '/Users/adithyapamulaparthy/Desktop/Courses_Spring2023/MedicalImageSegmentation/0522c0001/img.nrrd')
voxsz = [imgh['space directions'][0][0], imgh['space directions'][1][1], imgh['space directions'][2][2]]
d = displayvolume(img, voxsz, contrast=1500, level=500)
# d.display(slc=78)
# isosurface the bony structures using zero-padding to guarantee airtight, closed surface
print((np.array(np.shape(img)) + 2))

print((np.array(np.shape(img))))
imgzp = np.zeros((np.array(np.shape(img)) + 2))
imgzp[1:-1, 1:-1, 1:-1] = img

s = surface()
s.createSurfaceFromVolume(imgzp, voxsz, 700)

# un-zero pad the result
s.verts[:, 0] -= voxsz[0]
s.verts[:, 1] -= voxsz[1]
s.verts[:, 2] -= voxsz[2]

# mlab.figure(bgcolor=(1,1,1))
# s.display()

# find the connected components and display each with different colors
import matplotlib as mp

cols = mp.colormaps['jet']
surfaces = s.connectedComponents()
numsurf = np.size(surfaces)
print(f'Found {numsurf} components')

final_vol = 0
total_vol = 0
all_vol = []
for i in range(numsurf):
    spatial_value = surfaces[i].verts
    x = spatial_value[:, 0]
    y = spatial_value[:, 1]
    z = spatial_value[:, 2]
    for face in surfaces[i].faces:
        face = face.astype(np.int)
        vol = (-x[face[2]] * y[face[1]] * z[face[0]]) + \
              (x[face[1]] * y[face[2]] * z[face[0]]) + \
              (x[face[2]] * y[face[0]] * z[face[1]]) - \
              (x[face[0]] * y[face[2]] * z[face[1]]) - \
              (x[face[1]] * y[face[0]] * z[face[2]]) + \
              (x[face[0]] * y[face[1]] * z[face[2]])
        total_vol = (vol / 6) + total_vol
        final_vol = np.abs(total_vol)
    all_vol.append(final_vol)

vols = np.zeros(numsurf)
for i in range(numsurf):
    vols[i] = surfaces[i].volume()
    print(f'{i} {vols[i]}')

print("total vols")
# #
# # # find the component with the maximum volume and show it in magenta
maxvol = np.max(vols)
imax = np.argmax(vols)
print(f'Surface {imax} has max volume {maxvol}')

surfaces[imax].color = [1,0,1]
surfaces[imax].opacity = 1

mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
# ignore components smaller than 1000 mm^3 to perform connected component filtering
for i in range(numsurf):
    if vols[i] > 1000:
        surfaces[i].display()
mlab.show()


# convert the list to a pandas dataframe
df = pd.DataFrame(vols, columns=['values'])
# create the box plot using seaborn's boxplot function
sb.boxplot(data=df)
# set the title of the plot
plt.title('Box Plot of Sample Data')
plt.show()

while (1):
    d.fig.canvas.draw_idle()
    d.fig.canvas.start_event_loop(0.3)
