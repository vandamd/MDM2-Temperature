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
T10 = 15                                        # Initial temp of Room 1                   
To0 = 0                                         # Initial temp of outside the house
N = 24                                          # Number of hours in simulation
Xn = 5                                          # Number of points plotted per minute 
t = np.linspace(0, N*(60), (Xn*N*(60))+1)       
k_wall = 0.038                                
Cp_air = 1005
Cv_air = 718
air_density = 1.276                             # density of air
#alternative_outside_temp1 = -(1/1080)*math.sin(t/10800)                      # goes to -20 after 565 hours(23.5 days)
#alternative_outside_temp2 = (7/1440)*math.pi*math.sin((math.pi*t)/720)       # change of 7oC every 12 hrs
# ========================Dimensional variables==============================
L_room1 = 10
L_wall = 1
W_room1 = 10
Thickness_wall = 0.115             
H_room1 = 2
H_wall = 2
A_room1 = AreaCalc(L_room1,W_room1)
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
    dQ1dt = ((4*A_Wall_1_o)*(k_wall/Thickness_wall)*(To-T1)) + ((A_room1)*(k_wall/Thickness_wall)*(To-T1)) + 200
    dQodt = (7/1440)*math.pi*math.sin((math.pi*t)/720)

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
plt.plot(t, T1, 'g', lw = 2, label = 'Room temperature')
plt.plot(t, To, 'm', lw = 2, label = 'outside temperature')
plt.title('Temperature over time')
plt.legend()
plt.xlabel('Time(minutes)')
plt.ylabel('Temperature ($^\circ$C)')
plt.ylim(-0.5,T10+1)
plt.grid()
plt.show()