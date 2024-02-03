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

class OrcaFlexBatch:
    
    def __init__(self):
        #--------------------------------------------------------
        self.MODULUS_COPPER = 200e9           # E1
        self.MODULUS_STEEL = 110e9            # E2
        self.YIELD_STRENGTH_COPPER = 33e6     # Y1
        self.YIELD_STRENGTH_STEEL = 100e6     # Y2 data from web pages mostly (!) - could alter
        
        self.CONDUCTOR_RADIUS = 0
        self.ARMOUR_RADIUS = 0
        
        self.CONDUCTOR_AREA = 3492.6e-6     # A1 from Beier et al 2023 2.2.2 and (Nexans 2019 4.5.4)
        self.ARMOUR_AREA = 1024.9e-6         # A2
        
        
        # for 12 MW turbine, I=P/V=12e6/36e3 = 333.34A 
        # nearest is 342A in 150mm^2 conductor cable (Nexans 2019 4.5.4)
        
        #--------------------------------------------------------
        self.wave_type = None
        return

    def circular_area(self, radius):
        return math.pi*radius^2
    
    
    def second_moment_area_circle(self, radius):
        return math.pi/4 * radius^4
    
    
    def Kt1(self, A1,A2,E1,E2):       # Stress concentrator, calling 1 the conductor, the armour 2
        Kt1 = (1/(A1 + (A2*(E2/E1))))
        return Kt1
    
    
    def Kt2(self, A1,A2,E1,E2):
        #return 1/((A1*(E2/E1)) + A2)
        Kt2 = 1/((A1*(E2/E1)) + A2)
        return Kt2

    def set_regular_wave(self, model, wave_period: float, wave_height: float, wave_direction: float):
        environment = model.environment
    #dir 90°, 1.5m H, period T = 5s
        for wave_name in environment.WaveName:      # was doing thisoriginally to modify existing setup - TO CHANGE?
            print ("Name: " + str(wave_name))
            #environment.SelectedWaveTrain = wave_name
            environment.SelectedWave = wave_name
            environment.WaveDirection = wave_direction  # pj:0
            self.wave_direction = int(environment.WaveDirection)
            print ("Direction: " + str(environment.WaveDirection))
            #print ("Length: " + str(environment.WaveLength) + '\n')            
            environment.WavePeriod = wave_period    # pj:9
            self.wave_period = environment.WavePeriod
            print ("Period: " + str(self.wave_period))
            environment.WaveHeight = wave_height  # pj:5
            self.wave_height = environment.WaveHeight  # m
            print ("Height: " + str(self.wave_height))
            self.wave_type = "regular"
            return
    
    
    def set_JONSWAP_wave(self, model, wave_period: float, wave_hs: float, wave_direction: float):
        environment = model.environment
    #dir 90°, 1.5m H, period T = 5s
        for wave_name in environment.WaveName:      # was doing thisoriginally to modify existing setup - TO CHANGE?
            print ("Name: " + str(wave_name))
            #environment.SelectedWaveTrain = wave_name
            environment.SelectedWave = wave_name
            environment.WaveDirection = wave_direction  # pj:0
            self.wave_direction = int(environment.WaveDirection)
            print ("Direction: " + str(environment.WaveDirection))
            #print ("Length: " + str(environment.WaveLength) + '\n')
            environment.WaveType = "JONSWAP"
            environment.WavePeriod = wave_period    # pj:9
            self.wave_period = environment.WavePeriod
            print ("Period: " + str(self.wave_period))
            environment.WaveHeight = wave_height  # pj:5
            self.wave_height = environment.WaveHeight  # m
            print ("Height: " + str(self.wave_height))
            self.wave_type = "JONSWAP"
            return
    
    def print_batch_wave_data(self):
        if self.wave_type == "regular":
            print_regular_wave_data()
        elif self.wave_type == "JONSWAP":
            print_jonswap_wave_data()
        else:
            if self.wave_type != "" and self.wave_type != None:
                print("No print method defined for wave type ", self.wave_type)
            else:
                print("No wave type selected")
    
    def print_batch_regular_wave_data(self):    # report batch (not environment) wave values
        print ("Direction: " + str(self.wave_direction))
        print ("Period: " + str(self.wave_period))
        print ("Height: " + str(self.wave_height))
    
    def print_batch_jonswap_wave_data(self):    # report batch (not environment) wave values
        print ("Direction: " + str(self.wave_direction))
        print ("Period: " + str(self.wave_period))
        print ("Hs: " + str(self.wave_hs))

# =============================================================================
# def circular_area(radius):
#     return math.pi*radius^2
# 
# 
# def second_moment_area_circle(radius):
#     return math.pi/4 * radius^4
# 
# 
# def Kt1(A1,A2,E1,E2):       # Stress concentrator, calling 1 the conductor, the armour 2
#     Kt1 = (1/(A1 + (A2*(E2/E1))))
#     return Kt1
# 
# 
# def Kt2(A1,A2,E1,E2):
#     #return 1/((A1*(E2/E1)) + A2)
#     Kt2 = 1/((A1*(E2/E1)) + A2)
#     return Kt2
# =============================================================================





orcaflex_batch = OrcaFlexBatch()

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
# =============================================================================
# MODULUS_COPPER = 200e9           # E1
# MODULUS_STEEL = 110e9            # E2
# YIELD_STRENGTH_COPPER = 33e6     # Y1
# YIELD_STRENGTH_STEEL = 100e6     # Y2 data from web pages mostly (!) - could alter
# 
# CONDUCTOR_RADIUS = 0
# ARMOUR_RADIUS = 0
# 
# CONDUCTOR_AREA = 3492.6e-6     # A1 from Beier et al 2023 2.2.2 and (Nexans 2019 4.5.4)
# ARMOUR_AREA = 1024.9e-6         # A2
# =============================================================================


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


orcaflex_batch.set_regular_wave(model, 9, 1.5, 90)



# =============================================================================
# for wave_name in environment.WaveName:
#     print ("Name: " + str(wave_name))
#     #environment.SelectedWaveTrain = wave_name
#     environment.SelectedWave = wave_name
#     environment.WaveDirection = 90  # pj:0
#     print ("Direction: " + str(environment.WaveDirection))
#     print ("Period: " + str(environment.WavePeriod))
#     #print ("Length: " + str(environment.WaveLength) + '\n')
#     
#     environment.WavePeriod = 5.0    # pj:9
#     print ("Period: " + str(environment.WavePeriod))
#     
#     environment.WaveHeight = 1.5  # pj:5
#     initial_wave_height = environment.WaveHeight  # maybe have to get/read before any other environment variable set
# =============================================================================
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
        
# =============================================================================
# print("Wave direction: " + str(environment.WaveDirection))
# 
# initial_wave_direction = int(environment.WaveDirection)
# #initial_wave_height = environment.WaveHeight
# #initial_wave_hs print("environment.WaveHeight:" + str(environment.WaveHeight))
# print("initial_wave_height:" + str(initial_wave_height))
orcaflex_batch.print_batch_regular_wave_data()
# =============================================================================
# ======================================================== environment.WaveHs
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
#tension = array_cable.RangeGraph("Wall tension")
orcaflex_batch.tension = array_cable.RangeGraph("Wall tension")
print("tension: ",str(orcaflex_batch.tension))
# https://stackoverflow.com/a/36943813/11365317

# bend moment, shear forces, torsion moment, total load

#bend_moment = array_cable.RangeGraph("Bend moment")
orcaflex_batch.bend_moment = array_cable.RangeGraph("Bend moment")

print("Bend moment: ",str(orcaflex_batch.bend_moment))

#shear_force = array_cable.RangeGraph("Shear force")
orcaflex_batch.shear_force = array_cable.RangeGraph("Shear force")

print("Shear force: ",str(orcaflex_batch.shear_force))

#worst_zz_stress = array_cable.RangeGraph("Worst ZZ stress")
orcaflex_batch.worst_zz_stress = array_cable.RangeGraph("Worst ZZ stress")

print("ZZ stress: ",str(orcaflex_batch.worst_zz_stress))


    
finish_dateTime = datetime.now()

print("Finish time" + str(finish_dateTime))

sim_duration = model.simulationStopTime - model.simulationStartTime
print(str(sim_duration))


runtime_duration = finish_dateTime - start_dateTime

print("Runtime duration: ", str(runtime_duration))

#tension_history = array_cable.TimeHistory("Wall tension", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5))
orcaflex_batch.tension_history = array_cable.TimeHistory("Wall tension", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5))
print("Time history - Wall tension: ",str(orcaflex_batch.tension_history))

#bend_moment_history = array_cable.TimeHistory("Bend moment", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5))
orcaflex_batch.bend_moment_history = array_cable.TimeHistory("Bend moment", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5))
print("Bend moment history - Wall tension: ",str(orcaflex_batch.bend_moment_history))


# print all elements using list comprehension: [print (i) for i in bend_moment_history]

# calculate tension stress concentrators
orcaflex_batch.stress_concentrator_copper_1 = orcaflex_batch.Kt1(orcaflex_batch.CONDUCTOR_AREA, orcaflex_batch.ARMOUR_AREA, orcaflex_batch.MODULUS_COPPER, orcaflex_batch.MODULUS_STEEL)
orcaflex_batch.stress_concentrator_steel_2 = orcaflex_batch.Kt2(orcaflex_batch.CONDUCTOR_AREA, orcaflex_batch.ARMOUR_AREA, orcaflex_batch.MODULUS_COPPER, orcaflex_batch.MODULUS_STEEL)

print('Stress concentrator values \n copper: \t%f \nsteel: \t%f '%(orcaflex_batch.stress_concentrator_copper_1,orcaflex_batch.stress_concentrator_steel_2))
print(str(orcaflex_batch.stress_concentrator_copper_1))
print(str(orcaflex_batch.stress_concentrator_steel_2))

#TODO: calculate curvature stress concentrators

# calculate stresses over the time history    
orcaflex_batch.DBeier_stress_copper = np.multiply(orcaflex_batch.tension_history,orcaflex_batch.stress_concentrator_copper_1)
orcaflex_batch.DBeier_stress_steel = np.multiply(orcaflex_batch.tension_history,orcaflex_batch.stress_concentrator_steel_2)

# load concentrated stress history into dataframes
orcaflex_batch.DBeier_stress_copper_dataframe = pd.DataFrame(orcaflex_batch.DBeier_stress_copper)
orcaflex_batch.DBeier_stress_steel_dataframe = pd.DataFrame(orcaflex_batch.DBeier_stress_steel)

# plot stress history (against time) from dataframes
ax = orcaflex_batch.DBeier_stress_copper_dataframe.plot()
orcaflex_batch.DBeier_stress_steel_dataframe.plot(ax=ax)

plt.rcParams["figure.autolayout"] = True
plt.show()


orcaflex_batch.DBeier_rainflow_copper = rainflow.count_cycles(orcaflex_batch.DBeier_stress_copper)
orcaflex_batch.DBeier_rainflow_steel = rainflow.count_cycles(orcaflex_batch.DBeier_stress_steel)

print("Rainflow count of stresses for copper by D Beier method",str(orcaflex_batch.DBeier_rainflow_copper))

print("Finished")




#Beier_stress = 