#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 17:37:44 2018

@author: sathya
"""

import rawpy
import imageio
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

eleB=cv2.imread('babyelephant.jpg')
rows = eleB.shape[0]
clms = eleB.shape[1]
alpha=1000
gamma=2000

newfinal = eleB.copy()
for r in range(2, rows-3, 1):
    newrow=[]
    for c in range(2, clms-3, 1):
        Ix = eleB[r, c]
        for i in range(r-2, r+3, 1):
            num=[]
            e=[]
            for j in range(c-2, c+3, 1):
                if r!=i and c!=j:
                    Iy = eleB[i,j]
                    a = (math.exp((-math.sqrt((((r)-i)**2)+((c)-j)**2)) /alpha))
                    b = (math.exp(-(math.sqrt((Ix[0]-Iy[0])**2 + (Ix[1]-Iy[1])**2 + (Ix[2]-Iy[2])**2))/gamma))
                    numi = Iy*a*b
                    ep= a*b
                    e.append(ep)
                    num.append(numi)
                else:
                    pass
        den= sum(e)
        newIx = sum(num)/den
        newfinal[r,c] = newIx
    print r
plt.imshow(cv2.cvtColor(newfinal, cv2.COLOR_BGR2RGB))
plt.show()
cv2.imwrite('eleBilateral.png',newfinal)
