#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint 
import math
def Volumecalc(Le,Wi,He):
    '''Length, width and height'''
    V = Le*Wi*He
    return V


def thermalCapacitanceCalculator(p,V,c_p):
    """density, volume and specific heat"""
    C = p*V*c_p
    return C

# can use this to show any initial values for solutions, or for any constants that are in the differential equations            
# ========================Variable Initialisation==============================                      
Tp0 = 20
Ta0 = 16                                              
Tw0 = 10 
To0 = 0                 
t = np.linspace(0, 50, 10001)  
k_wall = 0.038
k_air = 0.02435

# ========================Dimensional variables==============================
L_wall = 1
L_air = 1
W_wall = 0.23
W_air = 1
H_wall = 1
H_air = 1

V_air = Volumecalc(L_air,W_air,H_air)
V_wall = Volumecalc(L_wall,W_wall,H_wall)
C_wall = thermalCapacitanceCalculator(600.5, V_wall, 2300)
C_air = thermalCapacitanceCalculator(1.276,V_air , 1.006)
# =============================================================================


#----------------------------------------------------------------------------#
#                             Differential equation
#----------------------------------------------------------------------------#
def Heat_model(y,t):
    """Creates all the differential equations 
       that are then integrated over time"""

    Tp,Ta,Tw,To = y
        
    ''' applied by Fouriers law, q = -k*del(T) as of now this shows change in energy, not temperature, since the RHS 
     of each equation is equal to the heat flux (which is flow of energy over time, dQdt).
     I think we can keep dQdt for conservation of energy for now to check that energy is conserved in a closed system.
     But to go from dQdt to dTdt we just divide by thermal capacity, like seen in Mikolaj's code.'''

    dQpdt = 0                        
    dQadt =  - k_air*(Ta-Tw) + k_air*(Tp-Ta)          
    dQwdt = k_wall*(Ta-Tw) - k_wall*(Tw-To) 
    dQodt = (7/24)*math.pi*math.sin((math.pi*t)/12)

    dTpdt = dQpdt
    dTadt = dQadt/C_air
    dTwdt = dQwdt/C_wall
    dTodt = dQodt

    return dTpdt, dTadt, dTwdt, dTodt

# This integrates all the derivatives over time, t
solution = odeint(Heat_model, [Tp0,Ta0,Tw0,To0], t)
Tp,Ta,Tw,To = solution.T



#----------------------------------------------------------------------------#
#                                 Plot
#----------------------------------------------------------------------------#


plt.figure()
plt.plot(t, Tp, 'g', lw = 2, label = 'Heater temperature')
plt.plot(t, Ta, 'b', lw = 2, label = 'Air temperature') 
plt.plot(t, Tw, 'r', lw = 2, label = 'Wall temperature') 
plt.plot(t, To, 'm', lw = 2, label = 'outside temperature')
plt.title('Temperature over time')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel('Time');
plt.ylabel('Temperature oC')
plt.grid()
plt.show()

