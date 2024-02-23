# -*- coding: utf-8 -*-
import OrcFxAPI
from datetime import datetime
import random
import math
import rainflow
import ffpack
import ffpack.fdm
import ffpack.lcc
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
        
        self.CONDUCTOR_RADIUS = 0.00725  # from a 14.5mm conductor (150mm^2)
        #self.ARMOUR_RADIUS = 0.0545      # 109.6mm overall outside diameter (150mm^2)
        self.ARMOUR_RADIUS = 0.01825      # screen diameter 36.5 (150mm^2)
# TODO: check - might want to change name to SCREEN_RADIUS?
        
        self.CONDUCTOR_AREA = 3492.6e-6     # A1 from Beier et al 2023 2.2.2 and (Nexans 2019 4.5.4)
        self.ARMOUR_AREA = 1024.9e-6         # A2
        
        
        # for 12 MW turbine, I=P/V=12e6/36e3 = 333.34A 
        # nearest is 342A in 150mm^2 conductor cable (Nexans 2019 4.5.4)
        # A=pi*r^2 so r=sqrt(A/pi)
        #--------------------------------------------------------
        self.wave_type = None
        return

    def circular_area(self, radius):
        return math.pi*radius**2
    
    
    def second_moment_area_circle(self, radius):
        return (math.pi/4) * (radius**4)
    
    
    def Kt1(self, A1,A2,E1,E2):       # Stress concentrator, calling 1 the conductor, the armour 2
        Kt1 = (1/(A1 + (A2*(E2/E1))))
        return Kt1
    
    
    def Kt2(self, A1,A2,E1,E2):
        #return 1/((A1*(E2/E1)) + A2)
        Kt2 = 1/((A1*(E2/E1)) + A2)
        return Kt2

    def Kc1(self, Y1, Cmax):
        Kc1 = Y1/Cmax
        return Kc1
    
    def Kc2(self, Y2, Cmax):    # could combine with Kc1, but Kt1 and Kt2 are currently separate also
        Kc2 = Y2/Cmax
        return Kc2
    


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
    
    
    def set_jonswap_wave(self, model, wave_period: float, wave_hs: float, wave_direction: float):
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
            environment.WaveHs = wave_hs  # pj:5
            self.wave_hs = environment.WaveHeight  # m
            print ("Hs: " + str(self.wave_hs))
            self.wave_type = "JONSWAP"     # maybe set above from environment?
            return
    
    def print_batch_wave_data(self):
        if self.wave_type == "regular":
            self.print_batch_regular_wave_data()
        elif self.wave_type == "JONSWAP":
            self.print_batch_jonswap_wave_data()
        else:
            if self.wave_type != "" and self.wave_type != None:
                print("No print method defined for wave type ", self.wave_type)
            else:
                print("No wave type selected")
    
    def print_batch_regular_wave_data(self):    # report batch (NB not environment) wave values
        print ("Direction: " + str(self.wave_direction))
        print ("Period: " + str(self.wave_period))
        print ("Height: " + str(self.wave_height))
    
    def print_batch_jonswap_wave_data(self):    # report batch (NB not environment) wave values
        print ("Direction: " + str(self.wave_direction))
        print ("Hs: " + str(self.wave_hs))
        
        
    def read_sn_csv(self):
        self.copper_sn = pd.read_csv("Copper SN - NS.csv").values.tolist()
        self.steel_sn = pd.read_csv("Steel SN - NS.csv").values.tolist()
        
    def calculate_damage(self, stress_time_series, material_sn):        # .orcaflex_batch.total_stress_1
        # rainflow = rainflow.count_cycles(stress_time_series)
        #orcaflex_batch.DBeier_rainflow_steel = rainflow.count_cycles(orcaflex_batch.total_stress_2)
        # no wait this is the non-ffpack way
    
        #print("Rainflow count of stresses for copper by D Beier method",str(rainflow))
    
        #self.read_sn_csv()    #need to pass in sn table read somehow
        print("copper_sn", str(material_sn))
        #print("steel_sn", str(self.steel_sn))
    
        #orcaflex_batch.rainflow_count = ffpack.lcc.astmRainflowCounting(orcaflex_batch.DBeier_tension_stress_copper)
        rainflow_count_material = ffpack.lcc.astmRainflowCounting(stress_time_series)
        print("rainflow_count_copper ", str(rainflow_count_material))
    
        # minerDamageModelClassic(lccData, snData, fatigueLimit)
        mp_damage = ffpack.fdm.minerDamageModelClassic(rainflow_count_material, material_sn, 100)    # Miner-Palmgren (mp) need to multiply by MPa (e6)
        print("copper_mp_damage ", str(mp_damage))
        return mp_damage


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

# set a regular wave
#orcaflex_batch.set_regular_wave(model, 9, 1.5, 90)

# set JONSWAP irregular waves
orcaflex_batch.set_jonswap_wave(model, 9, 1.5, 90)



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


# print whichever wave
orcaflex_batch.print_batch_wave_data()



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
orcaflex_batch.tension_history = array_cable.TimeHistory("Wall tension", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5))    # greatest tension at 0.5 metres (from observations)
print("Time history - Wall tension: ",str(orcaflex_batch.tension_history))

#bend_moment_history = array_cable.TimeHistory("Bend moment", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5))
orcaflex_batch.bend_moment_history = array_cable.TimeHistory("Bend moment", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5))    # greatest tension at 0.5 metres (from observations)
print("Bend moment history - Wall tension: ",str(orcaflex_batch.bend_moment_history))

orcaflex_batch.curvature_history = array_cable.TimeHistory("Curvature", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0))    # greatest curvature at 0 metres (from observations)

orcaflex_batch.curvature_x_history = array_cable.TimeHistory("x curvature", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0))    # greatest curvature at 0 metres (from observations)

orcaflex_batch.curvature_y_history = array_cable.TimeHistory("y curvature", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0))    # greatest curvature at 0 metres (from observations)

orcaflex_batch.x_bend_moment_history = array_cable.TimeHistory("x bend moment", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0))    # greatest (negative) bend moment at 0 metres (from observations)

Cmax = orcaflex_batch.curvature_history.max()
#Cxmax = orcaflex_batch.curvature_history.max()
#Cymax = orcaflex_batch.curvature_history.max()     # max of x and y curvature components not used?

# print all elements using list comprehension: [print (i) for i in bend_moment_history]

# calculate tension stress concentrators
orcaflex_batch.tension_stress_concentrator_copper_1 = orcaflex_batch.Kt1(orcaflex_batch.CONDUCTOR_AREA, orcaflex_batch.ARMOUR_AREA, orcaflex_batch.MODULUS_COPPER, orcaflex_batch.MODULUS_STEEL)
orcaflex_batch.tension_stress_concentrator_steel_2 = orcaflex_batch.Kt2(orcaflex_batch.CONDUCTOR_AREA, orcaflex_batch.ARMOUR_AREA, orcaflex_batch.MODULUS_COPPER, orcaflex_batch.MODULUS_STEEL)

orcaflex_batch.curvature_stress_concentrator_copper_1 = orcaflex_batch.Kc1(orcaflex_batch.YIELD_STRENGTH_COPPER, Cmax)
orcaflex_batch.curvature_stress_concentrator_steel_2 = orcaflex_batch.Kc2(orcaflex_batch.YIELD_STRENGTH_STEEL, Cmax)

# work out second moments of area
orcaflex_batch.I_second_moment_x_conductor = orcaflex_batch.second_moment_area_circle(orcaflex_batch.CONDUCTOR_RADIUS)
orcaflex_batch.I_second_moment_x_armour = orcaflex_batch.second_moment_area_circle(orcaflex_batch.ARMOUR_RADIUS) - orcaflex_batch.I_second_moment_x_conductor
# may want to change to 'screen' from 'armour'
# subtract inner (conductor) I from outer (screen/armour) full area I

print('Stress concentrator values \n copper: \t%f \nsteel: \t%f '%(orcaflex_batch.tension_stress_concentrator_copper_1,orcaflex_batch.tension_stress_concentrator_steel_2))
print(str(orcaflex_batch.tension_stress_concentrator_copper_1))
print(str(orcaflex_batch.tension_stress_concentrator_steel_2))

#TODO: calculate curvature stress concentrators

# calculate stresses over the time history    
orcaflex_batch.DBeier_tension_stress_copper = np.multiply(orcaflex_batch.tension_history,orcaflex_batch.tension_stress_concentrator_copper_1)   # Kt * T (element-wise)
orcaflex_batch.DBeier_tension_stress_steel = np.multiply(orcaflex_batch.tension_history,orcaflex_batch.tension_stress_concentrator_steel_2)
# TODO: supercede this

concentrated_tension_stress_1 = np.multiply(orcaflex_batch.tension_history,orcaflex_batch.tension_stress_concentrator_copper_1)   # Kt * T (element-wise)
concentrated_tension_stress_2 = np.multiply(orcaflex_batch.tension_history,orcaflex_batch.tension_stress_concentrator_steel_2)   # Kt * T (element-wise)

theta = 0   # (1) how do we know what angle is fatigue point location (max?) ? (2) should this be a class property?

curvature_components = np.subtract(np.multiply(orcaflex_batch.curvature_x_history,math.sin(theta)), np.multiply(orcaflex_batch.curvature_y_history,math.cos(theta)))
# curvature should be the same for both conductor _1 and armour _2 ?  TODO: CHECK THIS!!

concentrated_curvature_stress_1 = np.multiply(curvature_components, orcaflex_batch.curvature_stress_concentrator_copper_1)
concentrated_curvature_stress_2 = np.multiply(curvature_components, orcaflex_batch.curvature_stress_concentrator_steel_2)

orcaflex_batch.total_stress_1 = np.add(concentrated_tension_stress_1, concentrated_curvature_stress_1)   # element-wise addition of KtT + Kc(Cx*sin(th) - Cy*cos(th))
orcaflex_batch.total_stress_2 = np.add(concentrated_tension_stress_2, concentrated_curvature_stress_2)   # element-wise addition of KtT + Kc(Cx*sin(th) - Cy*cos(th))


# load concentrated stress history into dataframes
#orcaflex_batch.DBeier_tension_stress_copper_dataframe = pd.DataFrame(orcaflex_batch.DBeier_tension_stress_copper)
#orcaflex_batch.DBeier_tension_stress_steel_dataframe = pd.DataFrame(orcaflex_batch.DBeier_tension_stress_steel)
orcaflex_batch.DBeier_total_stress_copper_dataframe = pd.DataFrame(orcaflex_batch.total_stress_1)
orcaflex_batch.DBeier_total_stress_steel_dataframe = pd.DataFrame(orcaflex_batch.total_stress_2)

PThies_stress_copper = np.divide(orcaflex_batch.x_bend_moment_history, (orcaflex_batch.CONDUCTOR_RADIUS / orcaflex_batch.I_second_moment_x_conductor))  # (M_moment_x/I_second_moment_x)*centreline_distance

# D Beier and P Thies stress calcs candidates for refactoring as methods perhaps


# plot stress history (against time) from dataframes
#ax = orcaflex_batch.DBeier_tension_stress_copper_dataframe.plot()
#orcaflex_batch.DBeier_tension_stress_steel_dataframe.plot(ax=ax)

ax = orcaflex_batch.DBeier_total_stress_copper_dataframe.plot()
orcaflex_batch.DBeier_total_stress_steel_dataframe.plot(ax=ax)


plt.rcParams["figure.autolayout"] = True
plt.show()





#orcaflex_batch.DBeier_rainflow_copper = rainflow.count_cycles(orcaflex_batch.DBeier_tension_stress_copper)
#orcaflex_batch.DBeier_rainflow_steel = rainflow.count_cycles(orcaflex_batch.DBeier_tension_stress_steel)
#orcaflex_batch.DBeier_rainflow_copper = rainflow.count_cycles(orcaflex_batch.total_stress_1)
#orcaflex_batch.DBeier_rainflow_steel = rainflow.count_cycles(orcaflex_batch.total_stress_2)


#print("Rainflow count of stresses for copper by D Beier method",str(orcaflex_batch.DBeier_rainflow_copper))


orcaflex_batch.read_sn_csv()            # read in SN curve data for copper and steel materials NB keep this
print("orcaflex_batch.copper_sn", str(orcaflex_batch.copper_sn))
print("orcaflex_batch_steel_sn", str(orcaflex_batch.steel_sn))

#orcaflex_batch.rainflow_count = ffpack.lcc.astmRainflowCounting(orcaflex_batch.DBeier_tension_stress_copper)
#orcaflex_batch.rainflow_count_copper = ffpack.lcc.astmRainflowCounting(orcaflex_batch.total_stress_1)
#print("orcaflex_batch.rainflow_count_copper ", str(orcaflex_batch.rainflow_count_copper))

#orcaflex_batch.copper_mp_damage = ffpack.fdm.minerDamageModelClassic(orcaflex_batch.rainflow_count_copper, orcaflex_batch.copper_sn, 100)    # Miner-Palmgren (mp) need to multiply by MPa (e6)
#print("orcaflex_batch.copper_mp_damage ", str(orcaflex_batch.copper_mp_damage))

damage_copper_dbeier = orcaflex_batch.calculate_damage(orcaflex_batch.total_stress_1, orcaflex_batch.copper_sn)
print("(from method) Damage:", damage_copper_dbeier)

print("Finished")



    
    


