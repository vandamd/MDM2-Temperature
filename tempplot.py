from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
import math

# --- Inputs ---
# T_desired = 25          # Constant
T_heater = 50           # Constant
# T_outside = 5           # Constant, will change
T = 10                  # *Changes* 
T_initial = 10
pi = math.pi

m_room_air = 1470       # Constant
M_heater = 3600         # Constant
c_air = 1005.4          # Constant
R = 4.329*10**(-7)      # Constant

t = np.linspace(0,24,100)


# --- Equations ----
def returns_dTdt(T, t):
    # Outside Temperature
    T_outside = (7/2 * math.sin(pi/12 * t - pi/2)) + (9 * math.cos(1/180 * t)) - 7.5

    # Heat Gain Equation
    dQgdt = (T_heater - T) * M_heater * c_air

    # Heat Loss Equation
    dQldt = (T - T_outside)/R

    # Changing Room Temperature Equation
    dTdt = (dQgdt - dQldt)/(m_room_air * c_air)

    return dTdt

T = odeint(returns_dTdt, T, t)


print(T)

plt.plot(t, T)
plt.xlabel('time (s)')
plt.ylabel('temperature (°C)')
plt.show()