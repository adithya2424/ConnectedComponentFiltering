import nibabel as nib
import numpy as np
import nrrd
import matplotlib.pyplot as plt
import numpy as np
from displayvol import *
from surface_adi_new import *
from mayavi import mlab
import pygame
import seaborn as sb
import pandas as pd

img = nib.load("/home-local/adi/scripts/pycharm_project_lobeseg/lobe_seg_downsampled/downsampled_inputs/582down.nii.gz")
sx, sy, sz = img.header.get_zooms()
voxsz = [sx, sy, sz]

# check the orientation of the image
print(nib.aff2axcodes(img.affine))

# set the image in " LAS " orientation
# pending code for setting the orientation: However, we can set the orientation #
a = np.array(img.dataobj, dtype="float32")
d = displayvolume(a, voxsz, contrast=1500, level=500)
d.display(slc=78)
# convert the input data to a tensor
img = a
print((np.array(np.shape(img)) + 2))

print((np.array(np.shape(img))))
imgzp = np.zeros((np.array(np.shape(img)) + 2))
imgzp[1:-1, 1:-1, 1:-1] = img
# Threshold the image
threshold = -600
binary_image = np.zeros_like(imgzp)
binary_image[imgzp > threshold] = 1
s = surface()
s.createSurfaceFromVolume(binary_image, voxsz, 0)

# un-zero pad the result
s.verts[:, 0] -= voxsz[0]
s.verts[:, 1] -= voxsz[1]
s.verts[:, 2] -= voxsz[2]

# find the connected components and display each with different colors
import matplotlib as mp

cols = mp.colormaps['jet']
surfaces = s.connectedComponents()
numsurf = np.size(surfaces)
print(f'Found {numsurf} components')

mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
for i in range(numsurf):
    surfaces[i].color = cols(0 % 256)[0:3]
    surfaces[i].opacity = 0.5
    surfaces[i].display()
mlab.show()

vols = s.volume(numsurf, surfaces)

# # # find the component with the maximum volume and show it in magenta
maxvol = np.max(vols)
imax = np.argmax(vols)
print(f'Surface {imax} has max volume {maxvol}')

surfaces[imax].color = [1,0,1]
surfaces[imax].opacity = 1

# mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
# # ignore components smaller than 1000 mm^3 to perform connected component filtering
# for i in range(numsurf):
#     if vols[i] > 1000:
#         surfaces[i].display()
# mlab.show()


while (1):
    d.fig.canvas.draw_idle()
    d.fig.canvas.start_event_loop(0.3)
