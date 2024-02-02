# -*- coding: utf-8 -*-
import OrcFxAPI
from datetime import datetime
import random
import math
import rainflow
import ffpack
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import spurioussadgjhasgdjasgd



def circular_area(radius):
    return math.pi*radius^2

def second_moment_area_circle(radius):
    return math.pi/4 * radius^4

def Kt1(A1,A2,E1,E2):       # Stress concentrator, calling 1 the conductor, the armour 2
    Kt1 = (1/(A1 + (A2*(E2/E1))))
    return Kt1

def Kt2(A1,A2,E1,E2):
    #return 1/((A1*(E2/E1)) + A2)
    Kt2 = 1/((A1*(E2/E1)) + A2)
    return Kt2


#model = OrcFxAPI.Model("MyFile.dat")

#model = OrcFxAPI.Model(r"C:\Users\pnj201\OneDrive - University of Exeter\3011 diss\diss orcaflex\Attempt 1 OrcaFlex tutorial attempt PNJ Oct 23\Attempt 1 OrcaFlex tutorial PNJ lines added.dat")
#model = OrcFxAPI.Model(r"C:\Users\pnj201\OneDrive - University of Exeter\3011 diss\diss orcaflex\Attempt 1 OrcaFlex tutorial attempt PNJ Oct 23\Attempt 1 OrcaWave tutorial PNJ xz maybe ok.owr")
model = OrcFxAPI.Model(r"C:\Users\pnj201\OneDrive - University of Exeter\3011 diss\coding copy of B Wotton material\TEST 1 - 30m\Subsea Cable 30m - 60 minutes.sim")
model = OrcFxAPI.Model(r"C:\Users\pnj201\OneDrive - University of Exeter\3011 diss\coding copy of B Wotton material\TEST 1 - 30m\Subsea Cable 30m.sim")

#umaineSemiPjType = model["Umaine semi PJ type"]

#print("Type: " + str(type(umaineSemiPjType)))
#print(umaineSemiPjType.getmembers())       # list all members
#print ("Vessel Type Length: " + str(umaineSemiPjType.Length))
#umaineSemiPjType.Length = 88
#print ("Vessel Type Length: " + str(umaineSemiPjType.Length))

#--------------------------------------------------------
MODULUS_COPPER = 200e9           # E1
MODULUS_STEEL = 110e9            # E2
YIELD_STRENGTH_COPPER = 33e6     # Y1
YIELD_STRENGTH_STEEL = 100e6     # Y2 data from web pages mostly (!) - could alter

CONDUCTOR_RADIUS = 0
ARMOUR_RADIUS = 0

CONDUCTOR_AREA = 3492.6e-6     # A1 from Beier et al 2023 2.2.2 and (Nexans 2019 4.5.4)
ARMOUR_AREA = 1024.9e-6         # A2


# for 12 MW turbine, I=P/V=12e6/36e3 = 333.34A 
# nearest is 342A in 150mm^2 conductor cable (Nexans 2019 4.5.4)

#--------------------------------------------------------




#print("Beginning statics...")
#model.CalculateStatics()                # only calculates statics
#print("Beginning simulation...")
#model.RunSimulation()

start_dateTime = datetime.now()

print("Start time", str(start_dateTime))


for wave in model.waveComponents:
    print (wave)

model.SaveWaveSearchSpreadsheet("wavesearch1.xls")

#model.SaveSimulation("AutomatedPJ1.sim")

# https://www.orcina.com/webhelp/OrcFxAPI/Content/html/Pythoninterface,Objectdata.htm

environment = model.environment

#dir 90°, 1.5m H, period T = 5s

for wave_name in environment.WaveName:
    print ("Name: " + str(wave_name))
    #environment.SelectedWaveTrain = wave_name
    environment.SelectedWave = wave_name
    environment.WaveDirection = 90  # pj:0
    print ("Direction: " + str(environment.WaveDirection))
    print ("Period: " + str(environment.WavePeriod))
    #print ("Length: " + str(environment.WaveLength) + '\n')
    
    environment.WavePeriod = 5.0    # pj:9
    print ("Period: " + str(environment.WavePeriod))
    
    environment.WaveHeight = 1.5  # pj:5
    initial_wave_height = environment.WaveHeight  # maybe have to get/read before any other environment variable set
# =============================================================================
#     environment.WaveType = "JONSWAP"  # WaveType has to be set before Hs can be set
#     environment.WaveHs=5
#      
#     print ("Hs: " + str(environment.WaveHs))
#     environment.WaveHs=6
#     print ("Hs now: " + str(environment.WaveHs))
#     initial_wave_hs = environment.WaveHs
#     
#     print("initial_wave_hs:" + str(initial_wave_hs))
#     print ("Hs now (again): " + str(environment.WaveHs))
# =============================================================================
        
    print("Wave direction: " + str(environment.WaveDirection))
    
    initial_wave_direction = int(environment.WaveDirection)
    #initial_wave_height = environment.WaveHeight
    #initial_wave_hs = environment.WaveHs
    print("environment.WaveHeight:" + str(environment.WaveHeight))
    print("initial_wave_height:" + str(initial_wave_height))
# =============================================================================
#     print("initial_wave_hs:" + str(initial_wave_height))
# =============================================================================
    
#     for x in range(initial_wave_direction, initial_wave_direction + 180, 10):  # alter by 10 degrees until in reverse direction
#         environment.WaveDirection = environment.WaveDirection + 10
#         #environment.WaveHeight = initial_wave_height + random.randrange(-3,3)  # randomise wave height
#         environment.WaveHs = initial_wave_hs + random.randrange(-3,3)  # randomise wave significant  height
print("Beginning statics...")
model.CalculateStatics()                # only calculates statics
print("Beginning simulation...")
model.RunSimulation()
#         model.SaveWaveSearchSpreadsheet("wavesearch" + str(environment.WaveDirection) + ".xls")
#         print("Wave direction now: " + str(environment.WaveDirection))
#         #print("Wave height now: " + str(environment.WaveHeight))
#         print("Wave Hs now: " + str(environment.WaveHs))



completed_dateTime = datetime.now()

print("Simulation completed time: " + str(completed_dateTime))




array_cable = model["Array Cable"]

#tension = array_cable.RangeGraph("Wall tension",OrcFxAPI.SpecifiedPeriod(-8, 160))
tension = array_cable.RangeGraph("Wall tension")

print("tension: ",str(tension))


# bend moment, shear forces, torsion moment, total load

bend_moment = array_cable.RangeGraph("Bend moment")

print("Bend moment: ",str(bend_moment))

shear_force = array_cable.RangeGraph("Shear force")

print("Shear force: ",str(shear_force))

worst_zz_stress = array_cable.RangeGraph("Worst ZZ stress")

print("ZZ stress: ",str(worst_zz_stress))


    
finish_dateTime = datetime.now()

print("Finish time" + str(finish_dateTime))

sim_duration = model.simulationStopTime - model.simulationStartTime
print(str(sim_duration))


runtime_duration = finish_dateTime - start_dateTime

print("Runtime duration: ", str(runtime_duration))

tension_history = array_cable.TimeHistory("Wall tension", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5))
print("Time history - Wall tension: ",str(tension_history))

bend_moment_history = array_cable.TimeHistory("Bend moment", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5))
print("Bend moment history - Wall tension: ",str(bend_moment_history))

# print all elements using list comprehension: [print (i) for i in bend_moment_history]

# calculate tension stress concentrators
stress_concentrator_copper_1 = Kt1(CONDUCTOR_AREA, ARMOUR_AREA, MODULUS_COPPER, MODULUS_STEEL)
stress_concentrator_steel_2 = Kt2(CONDUCTOR_AREA, ARMOUR_AREA, MODULUS_COPPER, MODULUS_STEEL)

print('Stress concentrator values \n copper: \t%f \nsteel: \t%f '%(stress_concentrator_copper_1,stress_concentrator_steel_2))
print(str(stress_concentrator_copper_1))
print(str(stress_concentrator_steel_2))

#TODO: calculate curvature stress concentrators

# calculate stresses over the time history    
DBeier_stress_copper = np.multiply(tension_history,stress_concentrator_copper_1)
DBeier_stress_steel = np.multiply(tension_history,stress_concentrator_steel_2)

# load concentrated stress history into dataframes
DBeier_stress_copper_dataframe = pd.DataFrame(DBeier_stress_copper)
DBeier_stress_steel_dataframe = pd.DataFrame(DBeier_stress_steel)

# plot stress history (against time) from dataframes
DBeier_stress_copper_dataframe.plot()
DBeier_stress_steel_dataframe.plot()

plt.rcParams["figure.autolayout"] = True
plt.show()


DBeier_rainflow_copper = rainflow.count_cycles(DBeier_stress_copper)
DBeier_rainflow_steel = rainflow.count_cycles(DBeier_stress_steel)

print("Rainflow count of stresses for copper by D Beier method",str(DBeier_rainflow_copper))

print("Finished")


#Beier_stress = 