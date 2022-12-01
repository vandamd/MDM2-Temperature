#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 17:37:40 2022

@author: lewisvaughan
"""


from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
import math


T_outside= 5                # outside temp - take to be constat=nt 
T_room_initial= 15          # temperature of the room initially (at time t=0)
T_desired = 25              # the desired temperature we want the room to reach 
P_max_heater = 10 * 3600        # Constant, Power output of the heater - energy per second
mass_room_air = 1.2754      # Constant, in kg
c_air = 718                 # Constant, J/kg
U = 0.1 * 3600
A = 1
T_room = 15

t = np.linspace(0,24,500)
# dt = 1/60                 # Time interval for each minute
dt = t[1]-t[0]              # The time step

Ts_room = []
hour = 0
e = math.e
P_heater = 0
finished = 0

while T_room < T_desired:
    
    # Ramp-up of Heater
    if P_heater < P_max_heater:
        P_heater = e**(10*hour)
    elif P_heater == P_max_heater:
        P_heater = P_max_heater

    Q_heater = P_heater * dt
    Q_gain_from_heater = Q_heater

    T_room_from_gain = (Q_gain_from_heater/(mass_room_air*c_air)) + T_room_initial
    
    dQldt  = U * A * ( (T_room_from_gain+T_room_initial/2)-T_outside )
    
    T_room = (T_room_from_gain-T_room_initial) - ( (1/(mass_room_air*c_air) ) * dQldt*dt) + T_room_initial
    
    print(T_room)
    T_room_initial = T_room
    Ts_room.append(T_room)
    hour += dt

    if T_room >= T_desired:
        finished = 1


if finished == 1:

    newhour = 0

    while P_heater > 1:
        # Ramp-down of Heater
        if P_heater > 0:
            P_heater = e**(-7 * newhour + 10.49127)
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
        newhour += dt

hour = hour + newhour

time = np.linspace(0, hour, len(Ts_room))

plt.plot(time, Ts_room)
plt.xlabel('time (h)')
plt.ylabel('temperature (°C)')
plt.show()
    