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
T20 = 20                                        # Initial temp of Room 2
T30 = 12                                        # Initial temp of Room 3
To0 = 0                                         # Initial temp of outside the house
N = 1                                        # Number of hours in simulation
Xn = 5                                          # Number of points plotted per minute 
t = np.linspace(0, N*(60), (Xn*N*(60))+1) 
k_wall = 0.038
k_air = 0.02435
k_window = 0.96                                 # this is the value for glass, apparently lower for windows, needs looking into
Cp_air = 1005
Cv_air = 718
#alternative_outside_temp1 = -(1/144)*math.pi*math.sin((math.pi*t)/1440)     # goes to -20 after 1 day
#alternative_outside_temp2 = -(1/9)*math.sin(t/90)                           # goes to -20 after 283 minutes
# ========================Dimensional variables==============================
L_room1 = 10
L_room2 = 10 
L_room3 = 10
L_wall = 10
L_window = 0.7

W_room1 = 10
W_room3 = 10
W_room2 = 12.5
Thickness_wall = 0.23
Thickness_window = 0.00238                 # not sure if correct, different companies say different things

H_room1 = 2
H_room2 = 2
H_room3 = 2
H_wall = 2
H_window = 0.7

A_Window = AreaCalc(L_window,H_window)

V_room1 = VolumeCalc(L_room1,W_room1,H_room1)
V_room2 = VolumeCalc(L_room2,W_room2,H_room2)
V_room3 = VolumeCalc(L_room3,W_room3,H_room3)
C_room1 = thermalCapacitanceCalculator(1.276,V_room1 , Cv_air)
C_room2 = thermalCapacitanceCalculator(1.276,V_room2 , Cv_air)
C_room3 = thermalCapacitanceCalculator(1.276,V_room3 , Cv_air)

A_Wall_1_o = AreaCalc(W_room1,H_room1)
A_Wall_1_2 = AreaCalc(W_room1,H_room1)
A_Wall_2_o = AreaCalc(W_room2,H_room2)
A_Wall_3_2 = AreaCalc(W_room3,H_room3)
A_Wall_3_o = AreaCalc(W_room3,H_room3)
V_wall = VolumeCalc(L_wall,Thickness_wall,H_wall)
C_wall = thermalCapacitanceCalculator(600.5, V_wall, 2300)
# =============================================================================

# Prints the values of the thermal capacity of each room
#print('C_room1 =',C_room1,'\nC_room2 =',C_room2,'\nC_room3 =',C_room3)

#----------------------------------------------------------------------------#
#                             Differential equation
#----------------------------------------------------------------------------#
def Heat_model(y,t):
    """Creates all the differential equations 
       that are then integrated over time"""

    T1,T2,T3,To = y
        
    ''' applied by Fouriers law, q = -k*del(T) as of now this shows change in energy, not temperature, since the RHS 
     of each equation is equal to the heat flux (which is flow of energy over time, dQdt)'''

    # Net heat flow for every room                        
    dQ1dt = ((2*A_Wall_1_o)*(k_wall/Thickness_wall)*(To-T1)) + ((A_Wall_1_o - A_Window)*(k_wall/Thickness_wall)*(To-T1)) + (
        (A_Window)*(k_window/Thickness_window)*(To-T1)) + ((A_Wall_1_2)*(k_wall/Thickness_wall)*(T2-T1))  

    dQ2dt = ((A_Wall_1_2)*(k_wall/Thickness_wall)*(T1-T2)) + ((A_Wall_3_2)*(k_wall/Thickness_wall)*(T3-T2)) + ((2*A_Wall_2_o)*(k_wall/Thickness_wall)*(To-T2)) 
    dQ3dt = ((A_Wall_3_2)*(k_wall/Thickness_wall)*(T2-T3)) + ((3*A_Wall_3_o)*(k_wall/Thickness_wall)*(To-T3)) 
    dQodt = (7/240)*math.pi*math.sin((math.pi*t)/120)
    # rate of change of temperature for each room
    dT1dt = (dQ1dt/C_room1)*60
    dT2dt = (dQ2dt/C_room2)*60
    dT3dt = (dQ3dt/C_room3)*60
    dTodt = (dQodt)

    return dT1dt, dT2dt, dT3dt, dTodt

# This integrates all the derivatives over time, t
solution = odeint(Heat_model, [T10,T20,T30,To0], t)
T1,T2,T3,To = solution.T



#----------------------------------------------------------------------------#
#                                 Plot
#----------------------------------------------------------------------------#

plt.figure()
plt.plot(t, T1, 'g', lw = 2, label = 'Left room temp')
plt.plot(t, T2, 'b', lw = 2, label = 'Middle room temp') 
plt.plot(t, T3, 'r', lw = 2, label = 'Right room temp') 
plt.plot(t, To, 'm', lw = 2, label = 'outside temperature')
plt.title('Temperature over time')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel('Time(minutes)');
plt.ylabel('Temperature ($^\circ$C)')
plt.grid()
plt.show()