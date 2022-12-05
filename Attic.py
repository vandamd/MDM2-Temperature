#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint 
import math

def AreaCalc(Length,Height):
    '''Length and height'''
    A = Length*Height
    return A

def VolumeCalc(Length,Width,Height):
    '''Length, width and height'''
    V = Length*Width*Height
    return V

def thermalCapacitanceCalculator(p,V,c_p):
    """density, volume and specific heat"""
    C = p*V*c_p
    return C

# can use this to show any initial values for solutions, or for any constants that are in the differential equations            
# ========================Variable Initialisation==============================                      
T10 = 15                                        # Initial temp of Room 1                   
T20 = 20                                        # Initial temp of Room 2
T30 = 15                                        # Initial temp of Room 3  
Ta0 = 10                                        # Initial temp of the attic                
To0 = 0                                         # Initial temp of outside the house
Tb0 = 15                                        # Initial temp of the basement
Tins1_0 = 15                                    # Initial temp of insulation 1
Tins2_0 = 15                                    # Initial temp of insulation 2
Tins3_0 = 15                                    # Initial temp of insulation 3
Tins4_0 = 15                                    # Initial temp of insulation 4
Tg0 = 8                                         # Initial temp of the ground beneath the house

N = 10                                          # Number of hours in simulation
Xn = 5                                          # Number of points plotted per minute 
t = np.linspace(0, N*(60), (Xn*N*(60))+1) 
k_wall = 0.038                                  # Thermal conductivity of wood
k_air = 0.02435                                 # Thermal conductivity of air
Cp_air = 1005                                   # specific heat capacity of air at constant pressure
Cv_air = 718                                    # specific heat capacity of air at constant volume
air_density = 1.276                             # density of air
insulation_density = 30                         # density of the insulation

total_geothermal_power = 0                      # power output of the generator
basement_power = 0.1*total_geothermal_power     # energy from generator not going into air vents
rooms_power = (0.9*total_geothermal_power)/3    # accounting for some radiation
#alternative_outside_temp1 = -(1/1080)*math.sin(t/10800)                      # goes to -20 after 565 hours(23.5 days)
#alternative_outside_temp2 = (7/1440)*math.pi*math.sin((math.pi*t)/720)       # change of 7oC every 12 hrs
# ========================Dimensional variables==============================
L_room1 = 10
L_room2 = 10 
L_room3 = 10
L_wall = 10
L_insulation_1 = 32.5
L_insulation_2 = 10
L_insulation_3 = 32.5
L_insulation_4 = 10


W_room1 = 10
W_room2 = 12.5
W_room3 = 10
W_house = 32.5
W_insulation = 0.07
Thickness_wall = 0.23
Insulation_wall_thickness = 0.115 

H_wall = 2
H_roof = 2
slope_length = math.sqrt((H_roof)**2 + (W_house/2)**2)

A_room1 = AreaCalc(L_room1,W_room1)
A_room2 = AreaCalc(L_room2,W_room2)
A_room3 = AreaCalc(L_room3,W_room3)
V_room1 = VolumeCalc(L_room1,W_room1,H_wall)
V_room2 = VolumeCalc(L_room2,W_room2,H_wall)
V_room3 = VolumeCalc(L_room3,W_room3,H_wall)
C_room1 = thermalCapacitanceCalculator(air_density,V_room1 , Cv_air)
C_room2 = thermalCapacitanceCalculator(air_density,V_room2 , Cv_air)
C_room3 = thermalCapacitanceCalculator(air_density,V_room3 , Cv_air)

V_insulation_1 = VolumeCalc(L_insulation_1,W_insulation,H_wall)
V_insulation_2 = VolumeCalc(L_insulation_2,W_insulation,H_wall)
V_insulation_3 = VolumeCalc(L_insulation_3,W_insulation,H_wall)
V_insulation_4 = VolumeCalc(L_insulation_4,W_insulation,H_wall)
C_insulation_1 = thermalCapacitanceCalculator(insulation_density,V_insulation_1,Cv_air)
C_insulation_2 = thermalCapacitanceCalculator(insulation_density,V_insulation_2,Cv_air)
C_insulation_3 = thermalCapacitanceCalculator(insulation_density,V_insulation_3,Cv_air)
C_insulation_4 = thermalCapacitanceCalculator(insulation_density,V_insulation_4,Cv_air)

A_Wall_1_o = AreaCalc(W_room1,H_wall)
A_Wall_1_2 = AreaCalc(W_room1,H_wall)
A_Wall_2_o = AreaCalc(W_room2,H_wall)
A_Wall_3_2 = AreaCalc(W_room3,H_wall)
A_Wall_3_o = AreaCalc(W_room3,H_wall)
A_outside_wall_long = AreaCalc(L_insulation_1,H_wall)
A_outside_wall_short = AreaCalc(L_insulation_2,H_wall)

A_slope_roof = AreaCalc(W_room1,slope_length)
A_triangle = (1/2)*(W_house/2)*(H_roof)
V_attic = 2*A_triangle*W_room1
C_attic = thermalCapacitanceCalculator(air_density,V_attic,Cv_air)
# =============================================================================

#----------------------------------------------------------------------------#
#                             Differential equation
#----------------------------------------------------------------------------#

def Insulation_model(y,t):
    """Creates all the differential equations 
       that are then integrated over time"""

    T1,T2,T3,Ta,Tb,Tins1,Tins2,Tins3,Tins4,To,Tg = y

        
    ''' applied by Fouriers law, q = -k*del(T) as of now this shows change in energy, not temperature, since the RHS 
     of each equation is equal to the heat flux (which is flow of energy over time, dQdt)'''

    # Net heat flow for every room                        
    dQ1dt = ((A_Wall_1_2)*(k_wall/Insulation_wall_thickness)*(T2-T1)) + ((A_Wall_1_o)*(k_wall/Insulation_wall_thickness)*(Tins1-T1)) + ((A_Wall_1_o)*(k_wall/Insulation_wall_thickness)*(Tins4-T1)) + ((A_Wall_1_o)*(k_wall/Insulation_wall_thickness)*(Tins3-T1)) + ((A_room1)*(k_wall/Thickness_wall)*(Ta-T1)) + rooms_power
    dQ2dt = ((A_Wall_1_2)*(k_wall/Insulation_wall_thickness)*(T1-T2)) + ((A_Wall_3_2)*(k_wall/Insulation_wall_thickness)*(T3-T2)) + ((A_Wall_2_o)*(k_wall/Insulation_wall_thickness)*(Tins1-T2)) + ((A_Wall_2_o)*(k_wall/Insulation_wall_thickness)*(Tins3-T2)) + ((A_room2)*(k_wall/Thickness_wall)*(Ta-T2)) + ((A_room2)*(k_wall/Thickness_wall)*(Tb-T2)) + rooms_power
    dQ3dt = ((A_Wall_3_2)*(k_wall/Insulation_wall_thickness)*(T2-T3)) + ((A_Wall_3_o)*(k_wall/Insulation_wall_thickness)*(Tins1-T3)) + ((A_Wall_3_o)*(k_wall/Insulation_wall_thickness)*(Tins2-T3)) + ((A_Wall_3_o)*(k_wall/Insulation_wall_thickness)*(Tins3-T3)) + ((A_room3)*(k_wall/Thickness_wall)*(Ta-T3)) + rooms_power
    dQadt = ((A_room1)*(k_wall/Insulation_wall_thickness)*(T1-Ta)) + ((A_room2)*(k_wall/Thickness_wall)*(T2-Ta)) + ((A_room3)*(k_wall/Thickness_wall)*(T3-Ta)) + ((2*A_slope_roof)*(k_wall/Thickness_wall)*(To-Ta)) + ((4*A_triangle)*(k_wall/Thickness_wall)*(T3-Ta))
    dQbdt = ((A_room2)*(k_wall/Thickness_wall)*(T2-Tb)) +((A_room2)*(k_wall/Thickness_wall)*(Tg-Tb)) + ((4*A_Wall_1_2)*(k_wall/Thickness_wall)*(Tg-Tb)) + basement_power

    dQins1dt = ((A_Wall_1_o)*(k_wall/Insulation_wall_thickness)*(T1-Tins1)) + ((A_Wall_2_o)*(k_wall/Insulation_wall_thickness)*(T2-Tins1)) + ((A_Wall_3_o)*(k_wall/Insulation_wall_thickness)*(T3-Tins1)) + ((A_outside_wall_long)*(k_wall/Insulation_wall_thickness)*(To-Tins1))
    dQins2dt = ((A_Wall_3_o)*(k_wall/Insulation_wall_thickness)*(T3-Tins2)) + ((A_outside_wall_short)*(k_wall/Insulation_wall_thickness)*(To-Tins2)) 
    dQins3dt = ((A_Wall_1_o)*(k_wall/Insulation_wall_thickness)*(T1-Tins3)) + ((A_Wall_2_o)*(k_wall/Insulation_wall_thickness)*(T2-Tins3)) + ((A_Wall_3_o)*(k_wall/Insulation_wall_thickness)*(T3-Tins3)) + ((A_outside_wall_long)*(k_wall/Insulation_wall_thickness)*(To-Tins3))
    dQins4dt = ((A_Wall_3_o)*(k_wall/Insulation_wall_thickness)*(T1-Tins4)) + ((A_outside_wall_short)*(k_wall/Insulation_wall_thickness)*(To-Tins4))

    dQodt = 0 #+ (7/240)*math.pi*math.sin((math.pi*t)/120)
    dQgdt = 0
    # rate of change of temperature for each room
    dT1dt = (dQ1dt/C_room1)*60
    dT2dt = (dQ2dt/C_room2)*60
    dT3dt = (dQ3dt/C_room3)*60
    dTadt = (dQadt/C_attic)*60
    dTbdt = (dQbdt/C_room2)*60
    dTins1 = (dQins1dt/C_insulation_1)*60
    dTins2 = (dQins2dt/C_insulation_2)*60
    dTins3 = (dQins3dt/C_insulation_3)*60
    dTins4 = (dQins4dt/C_insulation_4)*60
    dTodt = (dQodt)
    dTgdt = (dQgdt)

    return dT1dt, dT2dt, dT3dt, dTadt, dTbdt, dTins1, dTins2, dTins3, dTins4, dTodt, dTgdt

# This integrates all the derivatives over time, t
solution = odeint(Insulation_model, [T10,T20,T30,Ta0,Tb0,Tins1_0,Tins2_0,Tins3_0,Tins4_0,To0,Tg0], t)
T1,T2,T3,Ta,Tb,Tins1,Tins2,Tins3,Tins4,To,Tg = solution.T
#----------------------------------------------------------------------------#
#                                 Plot
#----------------------------------------------------------------------------#

plt.figure()
plt.plot(t, T1, 'g', lw = 2, label = 'Left room temp')
plt.plot(t, T2, 'b', lw = 2, label = 'Middle room temp') 
plt.plot(t, T3, 'r', lw = 2, label = 'Right room temp') 
plt.plot(t, To, 'm', lw = 2, label = 'outside temp')
plt.plot(t, Ta, 'c', lw = 2, label = 'attic temp')
plt.plot(t, Tb, 'y', lw = 2, label = 'basement temp')
plt.plot(t, Tg, 'orange', lw = 2, label = 'ground temp')
#plt.plot(t, Tins1, 'y', lw = 2, label = 'Tins1')
#plt.plot(t, Tins2, 'c', lw = 2, label = 'Tins2')
#plt.plot(t, Tins3, 'k', lw = 2, label = 'Tins3')
#plt.plot(t, Tins4, 'm', lw = 2, label = 'Tins4')
plt.title('Temperature over time')
plt.legend()
plt.xlabel('Time(minutes)')
plt.ylabel('Temperature ($^\circ$C)')
plt.grid()
plt.show()