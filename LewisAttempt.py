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


T_outside= 5 #outside temp - take to be constat=nt 
T_room_initial= 15 #temperature of the room initially (at time t=0)
T_desired = 25 #the desired temperature we want the room to reach 
P_heater = 1500 #Power output of the heater - energy per second
mass_room_air = 1.2754 #in kg
c_air = 718 #in J/kg
U = 0.01
A = 1
T_room = 15


t = np.linspace(0,30,100)
dt = t[1]-t[0]
Q_heater = P_heater * dt
Q_gain_from_heater = Q_heater


while T_room < T_desired:
    
    T_room_from_gain = (Q_gain_from_heater/(mass_room_air*c_air)) + T_room_initial
    
    dQldt  = U * A * ( (T_room_from_gain+T_room_initial/2)-T_outside )
    
    T_room = (T_room_from_gain-T_room_initial) - ( (1/(mass_room_air*c_air) ) * dQldt*dt) + T_room_initial
    
    print(T_room)
    T_room_initial = T_room
    



    