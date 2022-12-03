#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint 
import math

def AreaCalc(Length,Height):
    '''Length and height'''
    A = Length*Height
    return A

def VolumeCalc(Length,Width,Height):
    '''Length, width and height'''
    V = Length*Width*Height
    return V

def thermalCapacitanceCalculator(p,V,c_p):
    """density, volume and specific heat"""
    C = p*V*c_p
    return C

# can use this to show any initial values for solutions, or for any constants that are in the differential equations            
# ========================Variable Initialisation==============================                      
T10 = 20                                        # Initial temp of Room 1                   
To0 = 0                                         # Initial temp of outside the house
N = 1                                          # Number of hours in simulation
Xn = 5                                          # Number of points plotted per minute 
t = np.linspace(0, N*(60), (Xn*N*(60))+1)       
k_wall = 0.038                                
Cp_air = 1005
Cv_air = 718
air_density = 1.276                             # density of air
#alternative_outside_temp1 = -(1/144)*math.pi*math.sin((math.pi*t)/1440)     # goes to -20 after 1 day
#alternative_outside_temp2 = -(1/9)*math.sin(t/90)                           # goes to -20 after 283 minutes
#alternative_outside_temp3 = (7/240)*math.pi*math.sin((math.pi*t)/120)
# ========================Dimensional variables==============================
L_room1 = 1
L_wall = 1
W_room1 = 1
Thickness_wall = 0.23               
H_room1 = 1
H_wall = 1
V_room1 = VolumeCalc(L_room1,W_room1,H_room1)
C_room1 = thermalCapacitanceCalculator(air_density,V_room1 , Cv_air)
A_Wall_1_o = AreaCalc(W_room1,H_room1)
# =============================================================================

#----------------------------------------------------------------------------#
#                             Differential equation
#----------------------------------------------------------------------------#
def Heat_model(y,t):
    """Creates all the differential equations 
       that are then integrated over time"""

    T1,To = y
        
    ''' applied by Fouriers law, q = -k*del(T) as of now this shows change in energy, not temperature, since the RHS 
     of each equation is equal to the heat flux (which is flow of energy over time, dQdt)'''

    # Net heat flow for every room                        
    dQ1dt = ((5*A_Wall_1_o)*(k_wall/Thickness_wall)*(To-T1)) 
    dQodt = 0

    # rate of change of temperature for each room
    dT1dt = (dQ1dt/C_room1)*60
    dTodt = (dQodt)

    return dT1dt, dTodt

# This integrates all the derivatives over time, t
solution = odeint(Heat_model, [T10,To0], t)
T1,To = solution.T

#----------------------------------------------------------------------------#
#                                 Plot
#----------------------------------------------------------------------------#

plt.figure()
plt.plot(t, T1, 'g', lw = 2, label = 'Left room temp')
plt.plot(t, To, 'm', lw = 2, label = 'outside temperature')
plt.title('Temperature over time')
plt.legend()
plt.xlabel('Time(minutes)')
plt.ylabel('Temperature ($^\circ$C)')
plt.grid()
plt.show()