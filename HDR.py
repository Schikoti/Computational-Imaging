#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 15:29:47 2018

@author: sathya
"""

import rawpy
import imageio
import cv2
import numpy as np
import matplotlib.pyplot as plt

'''
path = 'exposure1.nef'
raw=rawpy.imread(path)
rgb = raw.postprocess(gamma=(1 ,1),no_auto_bright=True,output_bps=16)
rgb1=rgb.astype('uint8')
rows=rgb1.shape[0]
clms=rgb1.shape[1]
clr=rgb1.shape[2]
print clr
rgb1new=cv2.cvtColor(rgb1, cv2.COLOR_BGR2RGB)
cv2.imwrite('processed_exposure1.tiff', rgb1new)
'''
HDR_zerosfinal = np.float32(np.zeros((201, 301, 3)))
wzfinal=np.float32(np.zeros((201, 301, 3)))
for l in range(1,17):
    LDR ="processed_exposure"+str(l)
    LDR_array=cv2.imread(LDR+'.tiff',-1)
    LDR_array=cv2.cvtColor(LDR_array, cv2.COLOR_BGR2RGB)
    LDR_downsampled=cv2.resize(LDR_array, None, fx=0.05, fy=0.05)
    rgb1new=np.multiply(LDR_downsampled,1.0/65535.0)
    t=(np.float32(2.0**(l-1))/2048.0)
    print t
    HDR_zeros = np.float32(np.zeros((201, 301, 3)))
    wz=np.float32(np.zeros((201, 301, 3)))
    for c in range(0, rgb1new.shape[2]):
        for i in range(0, rgb1new.shape[0]):
            for j in range(0,rgb1new.shape[1]):
               wz[i,j,c]=np.exp((-4*(rgb1new[i,j,c]-0.5)**2)/(0.5**2))
               HDR_zeros[i,j,c]=(np.multiply(wz[i,j,c], rgb1new[i,j,c]))/t
        print i
    HDR_zerosfinal+=HDR_zeros
    wzfinal+=wz
print 'wz_min',np.amin(wz)
#print 'HDR_zeros',HDR_zerosfinal[350:353,350:353]
#print 'wz',wz[350:353,350:353]
Ihdr=(HDR_zerosfinal*65535)/(wzfinal*65535)
#tonemap= cv2.createTonemapDurand(gamma=2.2, contrast=4.0,saturation=1.0,sigma_space=2.0,sigma_color=2.0)
#res_Ihdrtone = tonemap.process(Ihdr)
#res_Ihdrtone_8bit = np.clip(res_Ihdrtone*255, 0, 255).astype('uint8')
#print Ihdr.shape
Ihdr_tonemapped=Ihdr/(Ihdr+1)
#print 'Ihdr_tonemapped',Ihdr_tonemapped[350:353,350:353]
#Ihdr_final=np.multiply(Ihdr_tonemapped,65535)
#Ihdr_final8=np.uint8(Ihdr_tonemapped)
#print 'Ihdr_final',Ihdr_final[350:353,350:353]
plt.imshow(Ihdr_tonemapped)
plt.show()
#cv2.imwrite('HDR_phototonemap.png',res_Ihdrtone_8bit)