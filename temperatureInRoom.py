from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def thermalCapacitanceCalculator(p,v,c_p):
    """density, volume and specific heat"""
    C = p*v*c_p
    return C


#def conductionResistanceCalculator(L_t, A, k): 
#    """conduction resistance = thickness of surface / thermal conductivity * area of the surface"""
#    R_cond = L_t/k*A
#    return R_cond

#def convectiveResistanceCalculator(L_t, A, k): #same as conduction, don't really understand??
#    """convection resistance = thickness of surface / thermal conductivity * area of the surface"""
#   R_conv = L_t/(A*k)
#    return R_conv

#define constants
k_wall = 0.126
k_air = 0.02435
Lt_wall = 0.23
Lt_air = 1
A_wall = 1
A_air = 1
C_wall = thermalCapacitanceCalculator(600.5, 0.29*1*1*4, 2300)
C_air = thermalCapacitanceCalculator(1.276, 1, 1.006)

def airTemperatureChangeBasic(T,t,k_air,Lt_air, A_air, C_air):
    """energy rate of change = thermal conductivity * area of the surface / thickness of surface
    rate of change of temperature = energy rate of change / thermal capacitance""" 
    dqdt = (k_air*A_air/Lt_air) #equation for q, the heat transfer
    dTdt = dqdt/C_air #from Vandam's Equation (changing room temperature equation)
    return dTdt

def wallTemperatureChangeBasic(T,t,k_wall,Lt_wall, A_wall, C_wall):
    dqdt = (k_wall*A_wall/Lt_wall) #equation for q, the heat transfer
    dTdt = dqdt/C_wall #from Vandam's Equation (changing room temperature equation)
    return dTdt

initialTemp = [25]
t = np.linspace(0,20,200)

airResult = odeint(airTemperatureChangeBasic, initialTemp, t, args = (k_air, Lt_air, A_air, C_air))
wallResult = odeint(wallTemperatureChangeBasic, initialTemp, t, args = (k_wall, Lt_wall, A_wall, C_wall))
#outsideResult = odeint(outsideTemperatureChange, initalTemp, t,)

fig,ax = plt.subplots()
ax.plot(t,airResult,label='heater->air')
ax.plot(t,wallResult,label='air->wall')
#ax.plot(t,outsideResult,label='wall->outside')
ax.legend()
ax.set_xlabel('t')
ax.set_ylabel('T')
plt.show()
