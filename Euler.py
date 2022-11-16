#!/usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt


# ========================Variable Initialisation==============================
x0 = 0                                   # initial condion
y0 = 1                                   # initial condion
xf = 1                                   # upper limit of x
n = 21                                   # number of points 
n_true = 20*xf                           # number of points used for plotting the true solution
deltax = (xf-x0)/(n-1)                   # step size for each calculation
x = np.linspace(x0, xf, n)               # defining x-values
# =============================================================================


# initializing array for y-values
y = np.zeros ([n])

# creates points for the actual values of our equation
x_trueplot = np.linspace(x0,xf,20*xf)
y_true = np.exp(x_trueplot)
#----------------------------------------------------------------------------#
#                              Eulers Method
#----------------------------------------------------------------------------#
y [0] = y0
for i in range(1, n):
    y[i] = deltax*(y[i-1]) + y[i-1]


# prints values for x and y, can expand upon later to find error at each point
for i in range(n):
    print(x[i], y[i])

#----------------------------------------------------------------------------#
#                                   Plot
#----------------------------------------------------------------------------#
    
plt.figure()
plt.plot(x_trueplot,y_true)
plt.plot(x,y)
plt.xlabel('Value of x')
plt.ylabel('Value of y')
plt.title('Approximate solution with Forward Euler method')
plt.grid()
plt.legend(['True solution', 'Forward Euler solution'])
plt.show()
