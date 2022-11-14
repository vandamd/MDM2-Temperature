from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def thermalCapacitanceCalculator(p,v,c_p):
    """density, volume and specific heat"""
    C = p*v*c_p
    return C

C_air = thermalCapacitanceCalculator(1.276, 1, 1.006)
C_walls = thermalCapacitanceCalculator(600.5, 0.29*1*1*4, 2300)

def conductionResistanceCalculator(L_t, A, k): 
    """conduction resistance = thickness of surface / thermal conductivity * area of the surface"""
    R_cond = L_t/k*A
    return R_cond


def convectiveResistanceCalculator(L_t, A, k): #same as conduction, don't really understand??
    """convection resistance = thickness of surface / thermal conductivity * area of the surface"""
    R_conv = L_t/(A*k)
    return R_conv

def findingEnergyChangeBasic(t,k,L_t,A):
    """energy rate of change = thermal conductivity * area of the surface / thickness of surface""" 
    dqdt = (k*A/L_t) #equation for q, the heat transfer
    return dqdt


"""
def findingEnergyChangeWithResistance(t,k,L_t,A):
    k = 10 #thermal conductivity
    A = 1 #area of the surface
    L_t = 25 #thickness of surface
    dqdt = (k*A/L_t) #equation for q, the heat transfer
    return dqdt
"""

"""
k = [-2, 0, 1] #positive if trying to heat up room and negative if not
t = np.linspace(0,20,200)
woodEnergyChange = energyChange(t,0.126, 1, 0.23) #for a 1x1x1 room
result = odeint(energyChange,k,t,args=(k,))

fig,ax = plt.subplots()
ax.plot(t,result[:,0],label='k=-1')
ax.plot(t,result[:,1],label='k=0')
ax.plot(t,result[:,2],label='k=1')
ax.legend()
ax.set_xlabel('t')
ax.set_ylabel('T')
plt.show()
"""

"""Thermal capacitance C = mc_p"""
"""thermal behaviour is mainly influenced by convection and conduction"""
"""formula for heat transfer, q_cv: (kA/L_t)*(dt) where k is thermal conductivity, A is the area and L_t is the thickness in m"""