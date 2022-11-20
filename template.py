#!/usr/bin/env python
"""
This script runs a simulation of the COVID-19 pandemic by using differential
equations to model the rate of change of every variable at every time point. 
This model begins on the 4th of January 2021 is using British government 
data on the pandemic so it can better simulate what how severe the pandemic 
might get in this country.
The script can also be used to show a plot along with an animation
of the plot if a screenshot of the full plot is needed
All variables used can be edited in this 'Variable Initialisation' section 
below to change the plot and the animation given.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint 

# can use this to show any initial values for solutions, or for any constants that are in the differential equations            
# ========================Variable Initialisation==============================                      
Tp0 = 36
Ta0 = 0                                              
Tw0 = 20                  
t = np.linspace(0, 10000, 10001)  
q=1/3600       
k=1/1006
m=1/2300
# =============================================================================



#----------------------------------------------------------------------------#
#                             Differential equation
#----------------------------------------------------------------------------#
# make sure to swap out the variables here for ones we'll be using
def SIR_model(y,t):
    """Creates all the differential equations 
       that are then integrated over time
        
       In this SIR model we have added two differential 
       equations to make it slightly more realistic and 
       to add more variables that can be measured to track
       the progress of the virus"""

    Tp,Ta,Tw = y
        
    # can replace these equations for ones on temperature of each object(air, walls, etc.)  
    ''' applied by Fouriers law, q = -k*del(T) as of now this shows change in energy, not temperature, since the RHS 
     of each equation is equal to the heat flux (which is flow of energy over time, dQdt).
     I think we can keep dQdt for conservation of energy for now to check that energy is conserved in a closed system.
     But to go from dQdt to dTdt we just divide by thermal capacity, like seen in Mikolaj's code.'''
    dTpdt = q*(Ta-Tp)                         
    dTadt = k*(Tw-Ta) - k*(Ta-Tp)            
    dTwdt = m*(Ta-Tw) 

    return dTpdt, dTadt, dTwdt

# This integrates all the derivatives over time, t
# same thing applies here as said on line 37
solution = odeint(SIR_model, [Tp0,Ta0,Tw0], t)
Tp, Ta,Tw = solution.T



#----------------------------------------------------------------------------#
#                                 Plot
#----------------------------------------------------------------------------#


# can change these so they match variables in equations
plt.figure()
plt.plot(t, Tp, 'g', lw = 2, label = 'Person temperature')
plt.plot(t, Ta, 'b', lw = 2, label = 'Air temperature') 
plt.plot(t, Tw, 'r', lw = 2, label = 'Wall temperature') 
plt.title('Temperature over time')
plt.legend(loc = 'best')
plt.xlabel('Time');
plt.ylabel('Temperature oC')
plt.grid()
plt.ylim(0, 40)
plt.show()

