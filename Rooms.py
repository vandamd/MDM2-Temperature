#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint 
import math

def Volumecalc(Length,Width,Height):
    '''Length, width and height'''
    V = Length*Width*Height
    return V

def thermalCapacitanceCalculator(p,V,c_p):
    """density, volume and specific heat"""
    C = p*V*c_p
    return C

# can use this to show any initial values for solutions, or for any constants that are in the differential equations            
# ========================Variable Initialisation==============================                      
T10 = 15                                              
T20 = 20 
T30 = 15  
To0 = 0               
t = np.linspace(0, 50, 1001)  
k_wall = 0.038
k_air = 0.02435

# ========================Dimensional variables==============================
L_room1 = 10
L_room2 = 10 
L_room3 = 10
L_wall = 10

W_room1 = 10
W_room3 = 10
W_room2 = 12.5
W_wall = 0.23

H_room1 = 2
H_room2 = 2
H_room3 = 2
H_wall = 2


V_room1 = Volumecalc(L_room1,W_room1,H_room1)
V_room2 = Volumecalc(L_room2,W_room2,H_room2)
V_room3 = Volumecalc(L_room3,W_room3,H_room3)
C_room1 = thermalCapacitanceCalculator(1.276,V_room1 , 1.006)
C_room2 = thermalCapacitanceCalculator(1.276,V_room2 , 1.006)
C_room3 = thermalCapacitanceCalculator(1.276,V_room3 , 1.006)

V_wall = Volumecalc(L_wall,W_wall,H_wall)
C_wall = thermalCapacitanceCalculator(600.5, V_wall, 2300)
# =============================================================================


#----------------------------------------------------------------------------#
#                             Differential equation
#----------------------------------------------------------------------------#
def Heat_model(y,t):
    """Creates all the differential equations 
       that are then integrated over time"""

    T1,T2,T3,To = y
        
    ''' applied by Fouriers law, q = -k*del(T) as of now this shows change in energy, not temperature, since the RHS 
     of each equation is equal to the heat flux (which is flow of energy over time, dQdt).
     I think we can keep dQdt for conservation of energy for now to check that energy is conserved in a closed system.
     But to go from dQdt to dTdt we just divide by thermal capacity, like seen in Mikolaj's code.'''

    # Heat flow for every room                        
    dQ1dt = (k_wall/W_wall)*(To - T1) + (k_wall/W_wall)*(T2-T1)         
    dQ2dt = (k_wall/W_wall)*(T1-T2) + (k_wall/W_wall)*(T3-T2) 
    dQ3dt = (k_wall/W_wall)*(T2-T3) + (k_wall/W_wall)*(To - T3) 
    dQodt = (7/24)*math.pi*math.sin((math.pi*t)/12)

    # rate of change of temperature for each room
    dT1dt = dQ1dt/C_room1
    dT2dt = dQ2dt/C_room2
    dT3dt = dQ3dt/C_room3
    dTodt = dQodt

    return dT1dt, dT2dt, dT3dt, dTodt

# This integrates all the derivatives over time, t
solution = odeint(Heat_model, [T10,T20,T30,To0], t)
T1,T2,T3,To = solution.T



#----------------------------------------------------------------------------#
#                                 Plot
#----------------------------------------------------------------------------#
print('C_room1 =',C_room1,'\nC_room2 =',C_room2,'\nC_room3 =',C_room3)

plt.figure()
plt.plot(t, T1, 'g', lw = 2, label = 'Left room temp')
plt.plot(t, T2, 'b', lw = 2, label = 'Middle room temp') 
plt.plot(t, T3, 'r', lw = 2, label = 'Right room temp') 
plt.plot(t, To, 'm', lw = 2, label = 'outside temperature')
plt.title('Temperature over time')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel('Time');
plt.ylabel('Temperature oC')
plt.grid()
plt.show()