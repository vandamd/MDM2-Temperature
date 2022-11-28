#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 15:43:21 2022

@author: edatkinson
"""
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt



def model(Ta,T2,t):
    global dQdt

    dQdt = k0 * (T2 - Ta)
    
    
    return dQdt

def changeinheatloss(U, A, Ta, To):
    #loss through walls
    dQldt = U*A*(Ta - To)

    return dQldt


#def heatloss(dQldt, U, A, t):

    

Ta = 20 #starting temp
T2 = 25 #target temp
k0 = 1.28 * 1.006 #mass x cp
t = np.linspace(0,24,100)
To = 5
U = 10
A = 4



#To = outside temperature (constant for now)
#U= (k/d + hc + ho ) where k = thermal conductivity for the wall
#d = thickness of the wall, hc = thermal convection current inside, ho = convection outside.


result = odeint(model, k0, t, args=(k0,))


Ta = Ta + result
print(Ta)
#result2 = odeint(changeinheatloss, U*A, t, args=(U*A,)

                 

m = 1.28
c = 1.006


plt.plot(t, Ta)

