#!/usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt


# ========================Variable Initialisation==============================
x0 = 0                                   # initial condion
y0 = 20                                   # initial condion
xf = 4                                   # upper limit of x
n = 4000                                   # number of points 
n_true = 20*xf                           # number of points used for plotting the true solution
deltax = (xf-x0)/(n-1)                   # step size for each calculation
x = np.linspace(x0, xf, n)               # defining x-values

A_Wall_1_o = 1
k_wall = 0.038
Thickness_wall = 0.115
A_room1 = 1
# =============================================================================


# initializing array for y-values
y = np.zeros ([n])

#----------------------------------------------------------------------------#
#                              Eulers Method
#----------------------------------------------------------------------------#
y [0] = y0
for i in range(1, n):
    y[i] = deltax*((4*A_Wall_1_o)*(k_wall/Thickness_wall)*(-y[i-1]) + (A_room1)*(k_wall/Thickness_wall)*(-y[i-1]))+ y[i-1]


# prints values for x and y, can expand upon later to find error at each point
for i in range(n):
    print(x[i], y[i])

#----------------------------------------------------------------------------#
#                                   Plot
#----------------------------------------------------------------------------#
To = np.zeros ([n])     
plt.figure()
#plt.plot(x_trueplot,y_true)
plt.plot(x,y,'g', lw = 2, label = 'Room temperature')
plt.plot(x,To,'m', lw = 2, label = 'outside temperature')
plt.xlabel('Time(hours)')
plt.ylabel('Temperature($^\circ$C)')
plt.title('Approximate solution using Forward Euler method')
plt.ylim(-0.5,y0+1)
plt.grid()
plt.legend()
plt.show()
