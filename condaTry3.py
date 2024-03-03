# -*- coding: utf-8 -*-
import OrcFxAPI
from datetime import datetime
import copy
import random
import math
import rainflow
import ffpack
import ffpack.fdm
import ffpack.lcc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import rawdatx.read_TOA5 as read_raw_data
import rawdatx.process_XML as process_XML
import xlsxwriter
#import spurioussadgjhasgdjasgd

import orcaflex_batch

orcaflex_batch = orcaflex_batch.OrcaFlexBatch()

model = OrcFxAPI.Model(r"C:\Users\pnj201\OneDrive - University of Exeter\3011 diss\coding copy of B Wotton material\TEST 1 - 30m\Subsea Cable 30m - 60 minutes.sim")
model = OrcFxAPI.Model(r"C:\Users\pnj201\OneDrive - University of Exeter\3011 diss\coding copy of B Wotton material\TEST 1 - 30m\Subsea Cable 30m.sim")


#orcaflex_batch.read_wave_TOA5() # leave for the moment - ValueError: Object arrays cannot be loaded when allow_pickle=False
hs_t_df = orcaflex_batch.read_Hs_T()        # Hs and T in a dataframe
#hs_t_matrix, x_axis, y_axis, quad_mesh  = plt.hist2d(hs_t_df["Tm02_Avg"].values.tolist(), hs_t_df["Hm0_Avg"].values.tolist(), [range(orcaflex_batch.x_bins+1), range(orcaflex_batch.y_bins+1)])    # plot 2D matrix, using e.g. 10x10, save matrix values

hs_t_matrix, x_axis, y_axis, quad_mesh  = plt.hist2d(hs_t_df["tm02"].values.tolist(), hs_t_df["hm0"].values.tolist(), [range(orcaflex_batch.x_bins+1), range(orcaflex_batch.y_bins+1)])    # plot 2D matrix, using e.g. 10x10, save matrix values
# hs_t_matrix = (hs_t_matrix/hs_t_matrix.max()) # possibly unnecessary normalisation - and could use density parameter
# element 0 is 2x2 matrix, 1 and 2 are axes/bins, 3 is the QuadMesh

#mdir

# getting Hs:T for all directions (useful for info)

hs_t_matrix_rotated = np.rot90(hs_t_matrix, 1)  # in Hs(y axis) T(x) format for people to read
np.savetxt("Hs_T_matrix.csv", hs_t_matrix, delimiter=',')
np.savetxt("Hs_T_matrix_rotated.csv", hs_t_matrix_rotated, delimiter=',')


hs_t_df_list = orcaflex_batch.read_Hs_T_dir()        # Hs and T in a dataframe
#hs_t_matrix, x_axis, y_axis, quad_mesh  = plt.hist2d(hs_t_df["Tm02_Avg"].values.tolist(), hs_t_df["Hm0_Avg"].values.tolist(), [range(orcaflex_batch.x_bins+1), range(orcaflex_batch.y_bins+1)])    # plot 2D matrix, using e.g. 10x10, save matrix values

# getting Hs:T in a list filtered by direction

'''
hs_t_matrix_directional = [None] * len(hs_t_df_list)
x_axis_directional = [None] * len(hs_t_df_list)
y_axis_directional = [None] * len(hs_t_df_list)
quad_mesh_directional = [None] * len(hs_t_df_list)
hs_t_matrix_rotated_directional = [None] * len(hs_t_df_list)
'''

hs_t_matrix_directional = []
x_axis_directional = []
y_axis_directional = []
quad_mesh_directional = []
hs_t_matrix_rotated_directional = []

for i, hs_t_df in enumerate(hs_t_df_list):        # TODO: do this more pythonically
    hs_t_matrix, x_axis, y_axis, quad_mesh  = plt.hist2d(hs_t_df["tm02"].values.tolist(), hs_t_df["hm0"].values.tolist(), [range(orcaflex_batch.x_bins+1), range(orcaflex_batch.y_bins+1)])    # plot 2D matrix, using e.g. 10x10, save matrix values

# hs_t_matrix = (hs_t_matrix/hs_t_matrix.max()) # possibly unnecessary normalisation - and could use density parameter
# element 0 is 2x2 matrix, 1 and 2 are axes/bins, 3 is the QuadMesh

#mdir
    hs_t_matrix_directional.append(hs_t_matrix)
    x_axis_directional.append(x_axis)
    y_axis_directional.append(y_axis)
    quad_mesh_directional.append(quad_mesh)
    
    # TODO: CHECK THAT THESE ARE REALLY WORKING OK! Don't trust Python loops
    # (NB this matrix from matplotlib is sorta rotated)
    
    hs_t_matrix_rotated = np.rot90(hs_t_matrix, 1)  # in Hs(y axis) T(x) orientation for people to read
    hs_t_matrix_rotated_directional.append(hs_t_matrix_rotated)
    np.savetxt("Hs_T_matrix" + str(i) + ".csv", hs_t_matrix, delimiter=',')
    np.savetxt("Hs_T_matrix_rotated" + str(i) + ".csv", hs_t_matrix_rotated, delimiter=',')


start_dateTime = datetime.now()

print("Start time", str(start_dateTime))

# duration of Race Bank samples is 30 minutes
# Build list of direction, Hs, T tuples

dir_Hs_T = []

# for every dir (0=E, 1=S, 2=W, 3=N)
for direction_index, matrix in enumerate(hs_t_matrix_directional):
    for T_index, T in enumerate(matrix):
        for Hs_index, n in enumerate(T):
            if n > orcaflex_batch.n_threshold:
                #dir_Hs_T.append((direction_index, Hs_index, T_index, n))
                dir_Hs_T.append((direction_index, (x_axis_directional[direction_index][Hs_index] + x_axis_directional[direction_index][Hs_index+1])/2, (y_axis_directional[direction_index][T_index] + y_axis_directional[direction_index][T_index+1])/2, n))

# could have used a sparse-matrix/linked-list for all the zeroes

print("dir_Hs_T: ", str(dir_Hs_T))     # diagnostic
# (NB this matrix from matplotlib is sorta rotated)
# rows are T; columns are Hs 
# for every Hs
# for every T
# if greater than n_threshold
    # generate a wave of this Hs and T
    # run a simulation with this wave and multiply damage by the count of this Hs:T and dir



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





# print whichever wave
orcaflex_batch.print_batch_wave_data()



  
print("Beginning statics...")
model.CalculateStatics()                # only calculates statics
print("Beginning simulation...")
model.RunSimulation()

'''
model.ExtendSimulation(1800)            # run sim for extra half hour
model.RunSimulation()
'''

completed_dateTime = datetime.now()

print("Simulation completed time: " + str(completed_dateTime))




array_cable = model["Array Cable"]

orcaflex_batch.tension = array_cable.RangeGraph("Wall tension")
print("tension: ",str(orcaflex_batch.tension))
# https://stackoverflow.com/a/36943813/11365317

# bend moment, shear forces, torsion moment, total load

orcaflex_batch.bend_moment = array_cable.RangeGraph("Bend moment")

print("Bend moment: ",str(orcaflex_batch.bend_moment))

orcaflex_batch.shear_force = array_cable.RangeGraph("Shear force")

print("Shear force: ",str(orcaflex_batch.shear_force))

orcaflex_batch.worst_zz_stress = array_cable.RangeGraph("Worst ZZ stress")

print("ZZ stress: ",str(orcaflex_batch.worst_zz_stress))


    
finish_dateTime = datetime.now()

print("Finish time" + str(finish_dateTime))

sim_duration = model.simulationStopTime - model.simulationStartTime
print("Simulation duration: ", str(sim_duration))


runtime_duration = finish_dateTime - start_dateTime

print("Runtime duration: ", str(runtime_duration))

orcaflex_batch.tension_history = np.multiply(array_cable.TimeHistory("Wall tension", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5)), 1000)    # greatest tension at 0.5 metres (from observations) (kN) (*1e3 to SI)
print("Time history - Wall tension: ",str(orcaflex_batch.tension_history))

orcaflex_batch.bend_moment_history = np.multiply(array_cable.TimeHistory("Bend moment", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5)), 1000)    # greatest tension at 0.5 metres (from observations)  (kNm) (*1e3 to SI)
print("Bend moment history - Wall tension: ",str(orcaflex_batch.bend_moment_history))

orcaflex_batch.curvature_history = array_cable.TimeHistory("Curvature", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0))    # greatest curvature at 0 metres (from observations) in rad/m (SI)

orcaflex_batch.curvature_x_history = array_cable.TimeHistory("x curvature", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0))    # greatest curvature at 0 metres (from observations) in rad/m (SI)

orcaflex_batch.curvature_y_history = array_cable.TimeHistory("y curvature", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0))    # greatest curvature at 0 metres (from observations) in rad/m (SI)

#orcaflex_batch.x_bend_moment_history = np.multiply(array_cable.TimeHistory("x bend moment", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0)), 1000)    # greatest (negative) bend moment at 0 metres (from observations) (kNm) (*1e3 to SI)
orcaflex_batch.x_bend_moment_history = np.multiply(array_cable.TimeHistory("x bend moment", OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0)), 1)    # greatest (negative) bend moment at 0 metres (from observations) (kNm) (*1e3 to SI - or is it - code values unlike GUI may be in SI units Nm, so * 1) 

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
orcaflex_batch.DBeier_total_stress_copper_dataframe = pd.DataFrame(orcaflex_batch.total_stress_1)
orcaflex_batch.DBeier_total_stress_steel_dataframe = pd.DataFrame(orcaflex_batch.total_stress_2)


conductor_y = orcaflex_batch.CABLE_OUTER_DIAMETER / 4   # conductor centres approx half way out from cable centre (from diagram)

#PThies_stress_copper = np.divide(orcaflex_batch.x_bend_moment_history, (orcaflex_batch.CONDUCTOR_RADIUS / orcaflex_batch.I_second_moment_x_conductor))  # (M_moment_x/I_second_moment_x)*centreline_distance

PThies_stress_copper = np.multiply(np.divide(orcaflex_batch.x_bend_moment_history, orcaflex_batch.I_second_moment_x_conductor), conductor_y)  # (M_moment_x/I_second_moment_x)*centreline_distance

# https://stackoverflow.com/a/9171196/11365317

# D Beier and P Thies stress calcs candidates for refactoring as methods perhaps


ax = orcaflex_batch.DBeier_total_stress_copper_dataframe.plot()
orcaflex_batch.DBeier_total_stress_steel_dataframe.plot(ax=ax)


plt.rcParams["figure.autolayout"] = True
plt.show()


orcaflex_batch.read_sn_csv()            # read in SN curve data for copper and steel materials NB keep this
print("orcaflex_batch.copper_sn", str(orcaflex_batch.copper_sn))
print("orcaflex_batch_steel_sn", str(orcaflex_batch.steel_sn))


damage_copper_dbeier = orcaflex_batch.calculate_damage(orcaflex_batch.total_stress_1, orcaflex_batch.copper_sn)
print("(from method, for D Beier calc) Damage:", damage_copper_dbeier)

damage_copper_pthies = orcaflex_batch.calculate_damage(PThies_stress_copper, orcaflex_batch.copper_sn)
print("(from method, for P Thies calc) Damage:", damage_copper_pthies)

print("Finished")



    
    


