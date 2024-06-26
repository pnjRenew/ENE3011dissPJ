'''
CableFatigueDamageSims.py
Peter Jenkin 2024
A script to sample sea states from Race Bank North buoy data and run 
simulations to estimate fatigue damage on a model
'''

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
import csv


import orcaflex_batch

orcaflex_batch = orcaflex_batch.OrcaFlexBatch()

model = OrcFxAPI.Model(r"C:\Users\pnj201\OneDrive - University of Exeter\3011 diss\coding copy of B Wotton material\TEST 1 - 30m\Subsea Cable 30m - no current.sim")
# big path string - TODO: make this non-hard coded (command line argument?)

hs_t_df = orcaflex_batch.read_Hs_T()        # Hs and T in a dataframe
hs_t_matrix, x_axis, y_axis, quad_mesh  = plt.hist2d(hs_t_df["tm02"].values.tolist(), 
                                                     hs_t_df["hm0"].values.tolist(), 
                                                     [range(orcaflex_batch.x_bins+1), 
                                                      range(orcaflex_batch.y_bins+1)])    
# plot 2D matrix, using e.g. 10x10, save matrix values
# element 0 is 2x2 matrix, 1 and 2 are axes/bins, 3 is the QuadMesh
# getting Hs:T for all directions (useful for info)
hs_t_matrix_rotated = np.rot90(hs_t_matrix, 1)  
# in Hs(y axis) T(x) format for people to read
np.savetxt("Hs_T_matrix.csv", hs_t_matrix, delimiter=',')
np.savetxt("Hs_T_matrix_rotated.csv", hs_t_matrix_rotated, delimiter=',')


hs_t_df_list = orcaflex_batch.read_Hs_T_dir()        
# Hs and T in a dataframe                                                   
 # plot 2D matrix, using e.g. 10x10, save matrix values

# getting Hs:T in a list filtered by direction

'''
Initialise a load of variables, just in case
'''
hs_t_matrix_directional = []
x_axis_directional = []
y_axis_directional = []
quad_mesh_directional = []
hs_t_matrix_rotated_directional = []
individual_damage_scatter_table_dbeier = np.zeros((4,10,10))
scaled_damage_scatter_table_dbeier = np.zeros((4,10,10))
individual_damage_scatter_table_pthies = np.zeros((4,10,10))
scaled_damage_scatter_table_pthies = np.zeros((4,10,10))
df_individual_damage_scatter_table_dbeier = np.zeros((4))
df_scaled_damage_scatter_table_dbeier = np.zeros((4))
df_individual_damage_scatter_table_pthies = np.zeros((4))
df_scaled_damage_scatter_table_pthies = np.zeros((4))




for i, hs_t_df in enumerate(hs_t_df_list):        # TODO: do this more pythonically
    # line below for using tm02 for Tz    
    hs_t_matrix, x_axis, y_axis, quad_mesh  = plt.hist2d(hs_t_df["tm02"].values.tolist(), 
                                 hs_t_df["hm0"].values.tolist(), [range(orcaflex_batch.x_bins+1), 
                                  range(orcaflex_batch.y_bins+1)])    
                                # plot 2D matrix, using e.g. 10x10, save matrix values
    hs_t_matrix_directional.append(hs_t_matrix)
    x_axis_directional.append(x_axis)
    y_axis_directional.append(y_axis)
    quad_mesh_directional.append(quad_mesh)    
    # (NB this matrix from matplotlib is sorta rotated)    
    hs_t_matrix_rotated = np.rot90(hs_t_matrix, 1)  # in Hs(y axis) T(x) orientation for people to read
    hs_t_matrix_rotated_directional.append(hs_t_matrix_rotated)
    np.savetxt("Hs_T_matrix" + str(i) + ".csv", hs_t_matrix, delimiter=',')
    np.savetxt("Hs_T_matrix_rotated" + str(i) + ".csv", hs_t_matrix_rotated, delimiter=',')


start_dateTime = datetime.now()

print("Start time", str(start_dateTime))

# duration of Race Bank samples is 30 minutes
# Build list of direction, Hs, T tuples
dir_Hs_T_n = []
# for every dir (0=NE, 1=SE, 2=SW, 3=NW)
for direction_index, matrix in enumerate(hs_t_matrix_directional):
    for T_index, T in enumerate(matrix):
        for Hs_index, n in enumerate(T):
            if n > orcaflex_batch.n_threshold:
                dir_Hs_T_n.append((direction_index, (x_axis_directional[direction_index][Hs_index] + 
                 x_axis_directional[direction_index][Hs_index+1])/2, 
                   (y_axis_directional[direction_index][T_index] + 
                    y_axis_directional[direction_index][T_index+1])/2, n)) 
                # add direction, Hs:T & n data as tuple

# (could have used a sparse-matrix/linked-list for all the zeroes)

print("dir_Hs_T_n: ", str(dir_Hs_T_n))     # diagnostic

    # line below for using tm02 for Tz    
np.savetxt('directional_Hs_T_pairs.csv', dir_Hs_T_n, fmt= '%d', delimiter=',', header="dir,Hs,Tm02,n")
# (NB this matrix from matplotlib is sorta rotated)
# rows are T; columns are Hs 
# for every Hs
# for every T
# if greater than n_threshold
    # generate a wave of this Hs and T
    # run a simulation with this wave and multiply damage by the count of this Hs:T and dir



for wave in model.waveComponents:   # diagnostic
    print (wave)


# https://www.orcina.com/webhelp/OrcFxAPI/Content/html/Pythoninterface,Objectdata.htm

environment = model.environment

'''
Initialise batch counting variables
'''
damage_copper_pthies_total = 0
damage_copper_dbeier_total = 0
damage_steel_dbeier_total = 0

damage_copper_export_pthies = ["Hs_sim", "T_sim", "dir_sim", "n_sim", "damage_copper_pthies", 
                               "scaled_damage_copper_pthies", "damage_copper_pthies_total"]
damage_copper_export_dbeier = ["Hs_sim", "T_sim", "dir_sim", "n_sim", "damage_copper_dbeier", 
                               "scaled_damage_copper_dbeier","damage_copper_dbeier_total"]
damage_steel_export_dbeier = ["Hs_sim", "T_sim", "dir_sim", "n_sim", "damage_steel_dbeier", 
                              "scaled_damage_steel_dbeier", "damage_steel_dbeier_total"]

# overwrite any existing damage record file of this name
with open('damage_results_copper_pthies.csv', 'w', newline='') as csvfile:
    field_names = ["Hs_sim", "T_sim", "dir_sim", "n_sim", "damage_copper_pthies", 
                   "scaled_damage_copper_pthies","damage_copper_pthies_total"]
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()

with open('damage_results_copper_dbeier.csv', 'w', newline='') as csvfile:
    field_names = ["Hs_sim", "T_sim", "dir_sim", "n_sim", "damage_copper_dbeier", 
                   "scaled_damage_copper_dbeier","damage_copper_dbeier_total"]
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()
    # because using 'with', the file is closed, don't worry

with open('damage_results_steel_dbeier.csv', 'w', newline='') as csvfile:
    field_names = ["Hs_sim", "T_sim", "dir_sim", "n_sim", "damage_steel_dbeier",
                   "scaled_damage_steel_dbeier","damage_steel_dbeier_total"]    
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()
    # because using 'with', the file is closed, don't worry

with open('cable_simulation_results.csv', 'w', newline='') as csvfile:
    field_names = ["Hs_sim", "T_sim", "dir_sim", "n_sim", "dyn_y", "zz_stress", "bend_moment", 
                                                                   "tension", "curvature"]
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()
    # because using 'with', the file is closed, don't worry

all_sims_start_dateTime = datetime.now()



'''
Start batch simulations
'''

# this code is complementing that of orcaflex_batch.read_Hs_T_dir()
for  dir_Hs_T_n_tuple in dir_Hs_T_n:
    
    # let's try going at diagonals
    if dir_Hs_T_n_tuple[0] == 0:
        dir_sim = 45  
    elif dir_Hs_T_n_tuple[0] == 1:
        dir_sim = 135
    elif dir_Hs_T_n_tuple[0] == 2:
        dir_sim = 225
    elif dir_Hs_T_n_tuple[0] == 3:
        dir_sim = 315
    else:
        dir_sim = 0     # an error if not in cases! but default to 0 North
        
        
    Hs_sim = dir_Hs_T_n_tuple[1]
    T_sim = dir_Hs_T_n_tuple[2]
    n_sim = dir_Hs_T_n_tuple[3]

    # set JONSWAP irregular waves
    orcaflex_batch.set_jonswap_wave(model, T_sim, Hs_sim, dir_sim)


    print("T_sim, Hs_sim, dir_sim: ", T_sim, Hs_sim, dir_sim)
    # print whichever wave
    orcaflex_batch.print_batch_wave_data()
    
    
    
      
    print("Beginning statics...")
    model.CalculateStatics()                # only calculates statics
    print("Beginning simulation...")
    model.RunSimulation()
    
    sim_duration = model.simulationStopTime - model.simulationStartTime
    if sim_duration < 1800:                     
        # set to an extra half-hour only if not already extended
        model.ExtendSimulation(1800)            
        # run sim for extra half hour
        model.RunSimulation()                   
        # now run the simulation for that extended time too
    # TODO - alter model file manually to make this unnecessary
    
    completed_dateTime = datetime.now()    
    print("Simulation completed time: " + str(completed_dateTime))    
    model.SaveSimulation("./simfiles/BatchSimulation-" + str(Hs_sim) + "m_" + str(T_sim) + "s_" \
                         + str(n_sim) + "n_"  + str(dir_sim) + "dir" + "_" \
                         + all_sims_start_dateTime.strftime("%H-%M-%S_%d-%m-%Y") + ".sim")
    
    
    array_cable = model["Array Cable"]      # identify cable component in model
    
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
    orcaflex_batch.tension_history = np.multiply(array_cable.TimeHistory("Wall tension",
         OrcFxAPI.SpecifiedPeriod(
        model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5)), 1000)    
    # greatest tension at 0.5 metres (from observations) (kN) (*1e3 to SI)
    print("Time history - Wall tension: ",str(orcaflex_batch.tension_history))
    
    orcaflex_batch.bend_moment_history = np.multiply(array_cable.TimeHistory("Bend moment", 
         OrcFxAPI.SpecifiedPeriod(
        model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0.5)), 1000)    
    # greatest bend moment at 0.5 metres (from observations)  (kNm) (*1e3 to SI)
    print("Bend moment history - Wall tension: ",str(orcaflex_batch.bend_moment_history))
    
    orcaflex_batch.curvature_history = array_cable.TimeHistory("Curvature", OrcFxAPI.SpecifiedPeriod(
        model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0))    
    # greatest curvature at 0 metres (from observations) in rad/m (SI)    
    orcaflex_batch.curvature_x_history = array_cable.TimeHistory("x curvature", OrcFxAPI.SpecifiedPeriod(
        model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0))    
    # greatest curvature at 0 metres (from observations) in rad/m (SI)    
    orcaflex_batch.curvature_y_history = array_cable.TimeHistory("y curvature", OrcFxAPI.SpecifiedPeriod(
        model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0))    
    # greatest curvature at 0 metres (from observations) in rad/m (SI)
    #orcaflex_batch.x_bend_moment_history = np.multiply(array_cable.TimeHistory("x bend moment", 
    #OrcFxAPI.SpecifiedPeriod(model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0)), 
    #1000)    
    # greatest (negative) bend moment at 0 metres (from observations) (kNm) (*1e3 to SI)
    orcaflex_batch.x_bend_moment_history = np.multiply(array_cable.TimeHistory("x bend moment", 
       OrcFxAPI.SpecifiedPeriod(
        model.simulationStartTime,model.simulationStopTime),OrcFxAPI.oeArcLength(0)), 1)    
    # greatest (negative) bend moment at 0 metres (from observations) (kNm) 
    # (*1e3 to SI - or is it - code values unlike GUI may be in SI units Nm, so * 1) 
    
    Cmax = orcaflex_batch.curvature_history.max()
    #Cxmax = orcaflex_batch.curvature_history.max()
    #Cymax = orcaflex_batch.curvature_history.max()     # max of x and y curvature components not used?
    
    
    dyn_y = array_cable.RangeGraph("Dynamic y", OrcFxAPI.SpecifiedPeriod(
        model.simulationStartTime,model.simulationStopTime)).Max    
    dyn_y_df = pd.DataFrame(dyn_y)      # get maximum y (horizontal transverse to cable) movement for cable
    dyn_y_json = dyn_y_df.to_json()     # write to JSON string to fit in 1 column in saved CSV
    
    zz_stress = array_cable.RangeGraph("Worst ZZ stress", OrcFxAPI.SpecifiedPeriod(
        model.simulationStartTime,model.simulationStopTime)).Max
    zz_stress_df = pd.DataFrame(zz_stress)      # get maximum "worst" ZZ i.e. axial stress
    zz_stress_json = zz_stress_df.to_json()     # write to JSON string to fit in 1 column in saved CSV
    
    bend_moment = array_cable.RangeGraph("Bend moment", OrcFxAPI.SpecifiedPeriod(
        model.simulationStartTime,model.simulationStopTime)).Max
    bend_moment_df = pd.DataFrame(bend_moment)      
                                                # get maximum bend moment along cable sections/"arc lengths"
                                                    # through all simulation
    bend_moment_json = bend_moment_df.to_json()     # write to JSON string to fit in 1 column in saved CSV
    
    tension = array_cable.RangeGraph("Wall tension", OrcFxAPI.SpecifiedPeriod(
        model.simulationStartTime,model.simulationStopTime)).Max
    tension_df = pd.DataFrame(tension)      # get maximum tension throughout simulation throughout cable
    tension_json = tension_df.to_json()     # write to JSON string to fit in 1 column in saved CSV
    
    curvature = array_cable.RangeGraph("Curvature", OrcFxAPI.SpecifiedPeriod(
        model.simulationStartTime,model.simulationStopTime)).Max
    curvature_df = pd.DataFrame(curvature)      # get maximum curvature
    curvature_json = curvature_df.to_json()     # write to JSON string to fit in 1 column in saved CSV
    
    # print all elements using list comprehension: [print (i) for i in bend_moment_history]
    
    '''
    Stress concentrator calculations
    '''    
    
    # calculate tension stress concentrators
    orcaflex_batch.tension_stress_concentrator_copper_1 = orcaflex_batch.Kt1(
        orcaflex_batch.CONDUCTOR_AREA, orcaflex_batch.ARMOUR_AREA, orcaflex_batch.MODULUS_COPPER, 
        orcaflex_batch.MODULUS_STEEL)
    orcaflex_batch.tension_stress_concentrator_steel_2 = orcaflex_batch.Kt2(
        orcaflex_batch.CONDUCTOR_AREA, orcaflex_batch.ARMOUR_AREA, orcaflex_batch.MODULUS_COPPER, 
        orcaflex_batch.MODULUS_STEEL)
    
    #orcaflex_batch.curvature_stress_concentrator_copper_1 = orcaflex_batch.Kc1(
    #orcaflex_batch.YIELD_STRENGTH_COPPER, Cmax)
    #orcaflex_batch.curvature_stress_concentrator_steel_2 = orcaflex_batch.Kc2(
    #orcaflex_batch.YIELD_STRENGTH_STEEL, Cmax)
  
    orcaflex_batch.curvature_stress_concentrator_copper_1 = orcaflex_batch.Kc1(
        orcaflex_batch.YIELD_STRENGTH_COPPER)
    orcaflex_batch.curvature_stress_concentrator_steel_2 = orcaflex_batch.Kc2(
        orcaflex_batch.YIELD_STRENGTH_STEEL)
   
  
    # work out second moments of area
    orcaflex_batch.I_second_moment_x_conductor = orcaflex_batch.second_moment_area_circle(
        orcaflex_batch.CONDUCTOR_RADIUS)
    orcaflex_batch.I_second_moment_x_armour = orcaflex_batch.second_moment_area_circle(
        orcaflex_batch.ARMOUR_RADIUS) - orcaflex_batch.I_second_moment_x_conductor
    # may want to change to 'screen' from 'armour'
    # subtract inner (conductor) I from outer (screen/armour) full area I
    
    
    '''
    Stress calculations
    '''    
    
    print('Stress concentrator values \n copper: \t%f \nsteel: \t%f '%(
        orcaflex_batch.tension_stress_concentrator_copper_1,
        orcaflex_batch.tension_stress_concentrator_steel_2))
    print(str(orcaflex_batch.tension_stress_concentrator_copper_1))
    print(str(orcaflex_batch.tension_stress_concentrator_steel_2))
    
    
    
    # calculate stresses over the time history    
    orcaflex_batch.DBeier_tension_stress_copper = np.multiply(
        orcaflex_batch.tension_history,orcaflex_batch.tension_stress_concentrator_copper_1)   
    # Kt * T (element-wise)
    orcaflex_batch.DBeier_tension_stress_steel = np.multiply(
        orcaflex_batch.tension_history,orcaflex_batch.tension_stress_concentrator_steel_2)
    # TODO: supercede this
    
    concentrated_tension_stress_1 = np.multiply(orcaflex_batch.tension_history,
                                                orcaflex_batch.tension_stress_concentrator_copper_1)   
                                                # Kt * T (element-wise)
    concentrated_tension_stress_2 = np.multiply(orcaflex_batch.tension_history,
                                                orcaflex_batch.tension_stress_concentrator_steel_2)   
                                                # Kt * T (element-wise)    
    theta = 0   
    # (1) how do we know what angle is fatigue point location (max?) ? (2) should this be a class property?    
    curvature_components = np.subtract(np.multiply(orcaflex_batch.curvature_x_history,math.sin(theta)), 
               np.multiply(orcaflex_batch.curvature_y_history,math.cos(theta)))
    # curvature should be the same for both conductor _1 and armour _2 ?  TODO: CHECK THIS!!
    
    concentrated_curvature_stress_1 = np.multiply(curvature_components, 
                                                  orcaflex_batch.curvature_stress_concentrator_copper_1)
    concentrated_curvature_stress_2 = np.multiply(curvature_components, 
                                                  orcaflex_batch.curvature_stress_concentrator_steel_2)
    
    orcaflex_batch.total_stress_1 = np.add(concentrated_tension_stress_1, concentrated_curvature_stress_1)   
    # element-wise addition of KtT + Kc(Cx*sin(th) - Cy*cos(th))
    orcaflex_batch.total_stress_2 = np.add(concentrated_tension_stress_2, concentrated_curvature_stress_2)   
    # element-wise addition of KtT + Kc(Cx*sin(th) - Cy*cos(th))
    
    
    # load concentrated stress history into dataframes
    orcaflex_batch.DBeier_total_stress_copper_dataframe = pd.DataFrame(orcaflex_batch.total_stress_1)
    orcaflex_batch.DBeier_total_stress_steel_dataframe = pd.DataFrame(orcaflex_batch.total_stress_2)
    
    
    conductor_y = orcaflex_batch.CABLE_OUTER_DIAMETER / 4   
    # conductor centres approx half way out from cable centre (from diagram)
    
    #PThies_stress_copper = np.divide(orcaflex_batch.x_bend_moment_history, (
    #orcaflex_batch.CONDUCTOR_RADIUS / orcaflex_batch.I_second_moment_x_conductor))  
    # (M_moment_x/I_second_moment_x)*centreline_distance    
    #PThies_stress_copper = np.multiply(np.divide(
    #orcaflex_batch.x_bend_moment_history, orcaflex_batch.I_second_moment_x_conductor), conductor_y)  
    # (M_moment_x/I_second_moment_x)*centreline_distance
    
    
    # after removing current, where "x bend moment" became zero at the point (all points) when waves aligned,
    # change to using overall "bend moment"            
    PThies_stress_copper = np.multiply(np.divide(orcaflex_batch.bend_moment_history, 
                                                 orcaflex_batch.I_second_moment_x_conductor), conductor_y)  
                                                    # (M_moment_x/I_second_moment_x)*centreline_distance
    
    
    # https://stackoverflow.com/a/9171196/11365317
    
    # TODO: D Beier and P Thies stress calcs candidates for refactoring as methods perhaps
    
    
    ax = orcaflex_batch.DBeier_total_stress_copper_dataframe.plot()
    orcaflex_batch.DBeier_total_stress_steel_dataframe.plot(ax=ax)
    plt.rcParams["figure.autolayout"] = True
    plt.show()      # diagnostic plot of stresses
    
    
    orcaflex_batch.read_sn_csv()        # read in SN curve data for copper and steel materials NB keep this
    print("orcaflex_batch.copper_sn", str(orcaflex_batch.copper_sn))
    print("orcaflex_batch_steel_sn", str(orcaflex_batch.steel_sn))
    
    
    '''
    Damage functions call
    '''
    
    
    damage_copper_dbeier = orcaflex_batch.calculate_damage(orcaflex_batch.total_stress_1, 
                                                           orcaflex_batch.copper_sn, 
                                                           orcaflex_batch.FATIGUE_LIMIT_COPPER_NOMINAL)
    print("(from method, for D Beier calc) Damage:", damage_copper_dbeier)
    
    damage_copper_pthies = orcaflex_batch.calculate_damage(PThies_stress_copper, 
                                                           orcaflex_batch.copper_sn, 
                                                           orcaflex_batch.FATIGUE_LIMIT_COPPER_NOMINAL)
    print("(from method, for P Thies calc) Damage:", damage_copper_pthies)
    
    damage_steel_dbeier = orcaflex_batch.calculate_damage(orcaflex_batch.total_stress_2, 
                                                          orcaflex_batch.steel_sn, 
                                                          orcaflex_batch.FATIGUE_LIMIT_STEEL)
    print("(from method, for D BEeier (steel) calc) Damage:", damage_steel_dbeier)
    
    scaled_damage_copper_pthies = damage_copper_pthies * n_sim
    scaled_damage_copper_dbeier = damage_copper_dbeier * n_sim
    scaled_damage_steel_dbeier = damage_steel_dbeier * n_sim
    
    
    damage_copper_pthies_total = damage_copper_pthies_total + scaled_damage_copper_pthies
    damage_copper_dbeier_total = damage_copper_dbeier_total + scaled_damage_copper_dbeier
    damage_steel_dbeier_total = damage_steel_dbeier_total + scaled_damage_steel_dbeier

    # ought really to change this to print values from environment , including specifically Tz
    print("Sea state with Hs: ",Hs_sim , " and period T: ", T_sim, 
          " at direction: ",  dir_sim, " multiplied by occurrences n: ", n_sim, " doing individual damage", 
          damage_copper_pthies,  " together did total damage: ", scaled_damage_copper_pthies,
          "bringing running total P Thies damage to: ", damage_copper_pthies_total)
    print("Sea state with Hs: ",Hs_sim , " and period T: ", T_sim, 
          " at direction: ",  dir_sim, " multiplied by occurrences n: ", n_sim, " doing individual damage", 
          damage_copper_dbeier,  " together did total damage: ", scaled_damage_copper_dbeier, 
          "bringing running total D Beier damage to: ", damage_copper_dbeier_total)
    
    #save damage in appropriate cell (by Hs and Tp or Tm02/Tz) of appropriate matrix (by direction)
    individual_damage_scatter_table_dbeier[dir_Hs_T_n_tuple[0]][math.ceil(Hs_sim)-1][math.ceil(T_sim)-1] = \
                            damage_copper_dbeier
    scaled_damage_scatter_table_dbeier[dir_Hs_T_n_tuple[0]][math.ceil(Hs_sim)-1][math.ceil(T_sim)-1] = \
                            scaled_damage_copper_dbeier
    individual_damage_scatter_table_pthies[dir_Hs_T_n_tuple[0]][math.ceil(Hs_sim)-1][math.ceil(T_sim)-1] = \
                            damage_copper_pthies
    scaled_damage_scatter_table_pthies[dir_Hs_T_n_tuple[0]][math.ceil(Hs_sim)-1][math.ceil(T_sim)-1] = \
                            scaled_damage_copper_pthies    
    # rows being saved 'lowest from the top' so will want to flip vertically before saving as file
    
    
    damage_copper_export_pthies.append([Hs_sim, T_sim, dir_sim, n_sim, damage_copper_pthies, 
                                        scaled_damage_copper_pthies, damage_copper_pthies_total])
    damage_copper_export_pthies.append([Hs_sim, T_sim, dir_sim, n_sim, damage_copper_dbeier, 
                                        scaled_damage_copper_dbeier, damage_copper_dbeier_total])
    
    damage_steel_export_dbeier.append([Hs_sim, T_sim, dir_sim, n_sim, damage_steel_dbeier, 
                                       scaled_damage_steel_dbeier, damage_steel_dbeier_total])
    
    
    '''
    Write outputs to file (wrap things up)
    '''    
    
    with open('damage_results_copper_pthies.csv', 'a', newline='') as csvfile:
        field_names = ["Hs_sim", "T_sim", "dir_sim", "n_sim", "damage_copper_pthies", 
                       "scaled_damage_copper_pthies", "damage_copper_pthies_total"]
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writerow({'Hs_sim' : Hs_sim, 'T_sim' : T_sim, 'dir_sim' : dir_sim, 
                         'n_sim' : n_sim, 'damage_copper_pthies' : damage_copper_pthies, 
                         'scaled_damage_copper_pthies' : scaled_damage_copper_pthies, 
                         'damage_copper_pthies_total' : damage_copper_pthies_total})

    with open('damage_results_copper_dbeier.csv', 'a', newline='') as csvfile:
        field_names = ["Hs_sim", "T_sim", "dir_sim", "n_sim", "damage_copper_dbeier", 
                       "scaled_damage_copper_dbeier", "damage_copper_dbeier_total"]
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writerow({'Hs_sim' : Hs_sim, 'T_sim' : T_sim, 'dir_sim' : dir_sim, 
                         'n_sim' : n_sim, 'damage_copper_dbeier' : damage_copper_dbeier, 
                         'scaled_damage_copper_dbeier' : scaled_damage_copper_dbeier, 
                         'damage_copper_dbeier_total' : damage_copper_dbeier_total})
        # because using 'with', the file is closed, don't worry
    
    with open('damage_results_steel_dbeier.csv', 'a', newline='') as csvfile:
        field_names = ["Hs_sim", "T_sim", "dir_sim", "n_sim", "damage_steel_dbeier", 
                       "scaled_damage_steel_dbeier", "damage_steel_dbeier_total"]
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writerow({'Hs_sim' : Hs_sim, 'T_sim' : T_sim, 'dir_sim' : dir_sim, 
                         'n_sim' : n_sim, 'damage_steel_dbeier' : damage_steel_dbeier, 
                         'scaled_damage_steel_dbeier' : scaled_damage_steel_dbeier, 
                         'damage_steel_dbeier_total' : damage_steel_dbeier_total})
        # because using 'with', the file is closed, don't worry

    with open('cable_simulation_results.csv', 'a', newline='') as csvfile:
        field_names = ["Hs_sim", "T_sim", "dir_sim", "n_sim", "dyn_y", "zz_stress", 
                       "bend_moment", "tension", "curvature"]
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writerow({'Hs_sim' : Hs_sim, 'T_sim' : T_sim, 'dir_sim' : dir_sim, 
                         'n_sim' : n_sim, 'dyn_y' : dyn_y_json, 'zz_stress' : zz_stress_json, 
                         'bend_moment' : bend_moment_json, 'tension' : tension_json, 
                         'curvature' : curvature_json})
        # because using 'with', the file is closed, don't worry

'''
print CSV of results
at end of all sims
'''

# error https://stackoverflow.com/q/4674473/11365317 when trying to loop through
# so hard code indices for now

# for i in range(4):
    # df_individual_damage_scatter_table_dbeier[i] = pd.DataFrame(
    #     np.flip(individual_damage_scatter_table_dbeier[i],0))
    # df_scaled_damage_scatter_table_dbeier[i] = pd.DataFrame(
    #     np.flip(scaled_damage_scatter_table_dbeier[i],0))
    # df_individual_damage_scatter_table_pthies[i] = pd.DataFrame(
    #     np.flip(individual_damage_scatter_table_pthies[i],0))
    # df_scaled_damage_scatter_table_pthies[i] = pd.DataFrame(
    #     np.flip(scaled_damage_scatter_table_pthies[i],0))
    # # rows were saved 'lowest from the top' so will want to flip vertically before saving as file
    
    
    # df_individual_damage_scatter_table_dbeier[i].to_csv(
    #     "df_individual_damage_scatter_table_dbeier" + str(i) + ".csv")
    # df_scaled_damage_scatter_table_dbeier[i].to_csv(
    #     "df_scaled_damage_scatter_table_dbeier" + str(i) + ".csv")
    # df_individual_damage_scatter_table_pthies[i].to_csv(
    #     "df_individual_damage_scatter_table_pthies" + str(i) + ".csv")
    # df_scaled_damage_scatter_table_pthies[i].to_csv(
    #     "df_scaled_damage_scatter_table_pthies" + str(i) + ".csv")
    # save them

# comment-out for the moment, as may be buggy


pd.DataFrame(np.flip(individual_damage_scatter_table_dbeier[0],0)).to_csv(
                                    "individual_damage_scatter_dbeier_0.csv")
pd.DataFrame(np.flip(individual_damage_scatter_table_dbeier[1],0)).to_csv(
                                    "individual_damage_scatter_dbeier_1.csv")
pd.DataFrame(np.flip(individual_damage_scatter_table_dbeier[2],0)).to_csv(
                                    "individual_damage_scatter_dbeier_2.csv")
pd.DataFrame(np.flip(individual_damage_scatter_table_dbeier[3],0)).to_csv(
                                    "individual_damage_scatter_dbeier_3.csv")
pd.DataFrame(np.flip(scaled_damage_scatter_table_dbeier[0],0)).to_csv("scaled_damage_scatter_0_dbeier.csv")
pd.DataFrame(np.flip(scaled_damage_scatter_table_dbeier[1],0)).to_csv("scaled_damage_scatter_1_dbeier.csv")
pd.DataFrame(np.flip(scaled_damage_scatter_table_dbeier[2],0)).to_csv("scaled_damage_scatter_2_dbeier.csv")
pd.DataFrame(np.flip(scaled_damage_scatter_table_dbeier[3],0)).to_csv("scaled_damage_scatter_3_dbeier.csv")


pd.DataFrame(np.flip(individual_damage_scatter_table_pthies[0],0)).to_csv(
                                    "individual_damage_scatter_pthies_0.csv")
pd.DataFrame(np.flip(individual_damage_scatter_table_pthies[1],0)).to_csv(
                                    "individual_damage_scatter_pthies_1.csv")
pd.DataFrame(np.flip(individual_damage_scatter_table_pthies[2],0)).to_csv(
                                    "individual_damage_scatter_pthies_2.csv")
pd.DataFrame(np.flip(individual_damage_scatter_table_pthies[3],0)).to_csv(
                                    "individual_damage_scatter_pthies_3.csv")
pd.DataFrame(np.flip(scaled_damage_scatter_table_pthies[0],0)).to_csv("scaled_damage_scatter_0_pthies.csv")
pd.DataFrame(np.flip(scaled_damage_scatter_table_pthies[1],0)).to_csv("scaled_damage_scatter_1_pthies.csv")
pd.DataFrame(np.flip(scaled_damage_scatter_table_pthies[2],0)).to_csv("scaled_damage_scatter_2_pthies.csv")
pd.DataFrame(np.flip(scaled_damage_scatter_table_pthies[3],0)).to_csv("scaled_damage_scatter_3_pthies.csv")

all_sims_finish_dateTime = datetime.now()

print("Overall Finish time" + str(all_sims_finish_dateTime))
all_sims_runtime_duration = all_sims_finish_dateTime - all_sims_start_dateTime
print("Runtime duration: ", str(all_sims_runtime_duration))
print("Finished")



    
    


