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
import matplotlib.animation as animation

# can use this to show any initial values for solutions, or for any constants that are in the differential equations            
# ========================Variable Initialisation==============================
N = 68182137.0                          # Population of the UK
I0 = 521997.0                           # Initial infected
R0 = 0.0                                # Initial recovered
D0 = 79509.0                            # Initial death toll
S0 = N - I0 - R0 - D0                   # Total initially susceptible
t = np.linspace(0, 365, 366)            # Graph time steps (Days)
beta = 0.2                              # Contact rate
gamma = 1/14                            # Mean recovery rate (1/number of days)
d = 0.01                                # Probability of death
# =============================================================================



#----------------------------------------------------------------------------#
#                             Differential equation
#----------------------------------------------------------------------------#
# make sure to swap out the variables here for ones we'll be using
def SIR_model(y,t,N,beta,gamma,d):
    """Creates all the differential equations 
       that are then integrated over time
        
       In this SIR model we have added two differential 
       equations to make it slightly more realistic and 
       to add more variables that can be measured to track
       the progress of the virus"""

    S,I,R,D = y
        
    # can replace these equations for ones on temperature of each object(air, walls, etc.)        
    dSdt = -(beta * S * I / N) 
    dIdt = (beta * S * I / N) - (gamma * I) - (d * I) 
    dRdt = (gamma * I) 
    dDdt = (d * I)

    return dSdt, dIdt, dRdt, dDdt

# This integrates all the derivatives over time, t
# same thing applies here as said on line 37
solution = odeint(SIR_model, [S0, I0, R0, D0], t, args=(N,beta,gamma,d))
S,I,R,D = solution.T



#----------------------------------------------------------------------------#
#                                 Plot
#----------------------------------------------------------------------------#


# can change these so they match variables in equations
plt.figure()
plt.plot(t, S, 'b', lw = 2, label = 'Susceptible') 
plt.plot(t, I, 'r', lw = 2, label = 'Infected') 
plt.plot(t, R, 'g', lw = 2, label = 'Recovered') 
plt.plot(t, D, 'k', lw = 2, label = 'Dead')
plt.title('Epidemic over time')
plt.legend(loc = 'best')
plt.xlabel('Time (days)');
plt.ylabel('Population')
plt.grid()
plt.ylim(0, N)
plt.show()

