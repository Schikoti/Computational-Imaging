#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 21:33:35 2018

@author: sathya
"""


import rawpy
import imageio
import cv2
import numpy as np
import matplotlib.pyplot as plt

path = 'tetons.nef'
raw=rawpy.imread(path)
rawarray = raw.raw_image
rows = rawarray.shape[0]
clms= rawarray.shape[1]

red = rawarray[0::2,0::2]
blue = rawarray[1::2,1::2]
redN=(cv2.resize(red, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
blueN=(cv2.resize(blue, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
green = np.zeros((2872,4324))
raw_padded= np.pad(rawarray, 2, 'constant', constant_values=0)

for r in range(2, rows-2, 2):
    for c in range(2, clms-2, 2):
        dh = abs((rawarray[r,c-2]+rawarray[r,c+2])/2 - rawarray[r,c])
        dv = abs((rawarray[r-2,c]+rawarray[r+2,c])/2 - rawarray[r,c])
        if(dh>dv):
            green[r,c] = (rawarray[r-1,c]+rawarray[r+1,c])/2
        elif(dh<dv):
            green[r,c] = (rawarray[r,c-1]+rawarray[r,c+1])/2
        else:
            green[r,c] = (rawarray[r,c-1]+rawarray[r,c+1]+rawarray[r-1,c]+rawarray[r+1,c])/4
    print r
for r in range(3, rows-2, 2):
    for c in range(3, clms-2, 2):
        dh = abs((rawarray[r,c-2]+rawarray[r,c+2])/2 - rawarray[r,c])
        dv = abs((rawarray[r-2,c]+rawarray[r+2,c])/2 - rawarray[r,c])
        if(dh>dv):
            green[r,c] = (rawarray[r-1,c]+rawarray[r+1,c])/2
        elif(dh<dv):
            green[r,c] = (rawarray[r,c-1]+rawarray[r,c+1])/2
        else:
            green[r,c] = (rawarray[r,c-1]+rawarray[r,c+1]+rawarray[r-1,c]+rawarray[r+1,c])/4
    print r
for r in range(2, rows-2, 1):
    if(r%2==0):
        for c in range(3, clms-2, 2):
            green[r,c] = rawarray[r,c]
    else:
        for c in range(2, clms-2, 2):
            green[r,c] = rawarray[r,c]
            
green=green[2:-2:,2:-2:]

newfinal = np.dstack((redN,green,blueN))
newarray = np.uint8(np.array(newfinal)*255/np.max(np.array(newfinal)))
plt.imshow(newarray)
plt.show()
cv2.imwrite('tetons_dm.png', newarray)





