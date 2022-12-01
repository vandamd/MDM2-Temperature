from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
import math

# e for our exponential
e = math.e

# Initial Power of the heater before turning on
P_heater = 0

# If A is big enough, the heat loss will match heat gain so temperature will stabilise
A = 1

# Inputs:
#   T_room_initial = Temperature of the room at the when the heater needs to be turned off
#   T_desired = Temperature of the room you don't want to go lower than
#   P_heater_initial = Power of the heater when the heater needs to be turned off
#   dt = Time interval between data points

def heaterOFF(T_room_initial, T_desired, P_heater_initial, dt):

    # Variables
    T_outside = 5               # Will be changing
    P_max_heater = 10 * 3600    # Constant, Max power output of the heater - energy per second
    mass_room_air = 1.2754      # Constant, in kg
    c_air = 718                 # Constant, J/kg
    U = 0.1 * 3600              # Overall heat transfer coefficient
    Ts_room = []                # Array of temperatures calculated at each time interval
    hour = 0                    # A counter for how much time has passed (sum of time intervals)

    P_heater = P_heater_initial 
    T_room = T_room_initial  

    newhour = 0

    while P_heater > 1:
        # Ramp-down of Heater
        if P_heater > 0:
            P_heater = e**(10*hour) - 1
        else:
            break

        Q_heater = P_heater * dt
        Q_gain_from_heater = Q_heater

        T_room_from_gain = (Q_gain_from_heater/(mass_room_air*c_air)) + T_room_initial
        
        dQldt  = U * A * ( (T_room_from_gain+T_room_initial/2)-T_outside )
        
        T_room = (T_room_from_gain-T_room_initial) - ( (1/(mass_room_air*c_air) ) * dQldt*dt) + T_room_initial

        print(T_room)
        T_room_initial = T_room
        Ts_room.append(T_room)
        newhour -= dt

    hour = hour + newhour

    time = np.linspace(0, hour, len(Ts_room))

    return Ts_room, P_heater, hour

