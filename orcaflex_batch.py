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
import rawdatx.read_TOA5 as read_raw_data
import rawdatx.process_XML as process_XML
import xlsxwriter
#import spurioussadgjhasgdjasgd

class OrcaFlexBatch:
    
    def __init__(self):
        #--------------------------------------------------------
        # NB all units here should be SI, so m, Pa etc
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
        
        self.CABLE_OUTER_DIAMETER = 0.1096
        
        
        # for 12 MW turbine, I=P/V=12e6/36e3 = 333.34A 
        # nearest is 342A in 150mm^2 conductor cable (Nexans 2019 4.5.4)
        # A=pi*r^2 so r=sqrt(A/pi)
        #--------------------------------------------------------
        self.wave_type = None
        self.x_bins = 10
        self.y_bins = 10    # Hs:T wave sea state matrix bin edges (as integers) - could improve to decimals
        self.n_threshold = 0    # minimum n number of sea states for which to run simulation
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
    
        print("material_sn", str(material_sn))
    
        rainflow_count_material = ffpack.lcc.astmRainflowCounting(stress_time_series)
        print("rainflow_count_material ", str(rainflow_count_material))
    
        # minerDamageModelClassic(lccData, snData, fatigueLimit)     fatigueLimit 100?
        mp_damage = ffpack.fdm.minerDamageModelClassic(rainflow_count_material, material_sn, 1)    # Miner-Palmgren (mp) need to multiply by MPa (e6)
        print("material_mp_damage ", str(mp_damage))
        return mp_damage


    def read_wave_TOA5(self):
        rawdatx_config='./rawdatx_config.cfg'
        read_raw_data.main(rawdatx_config)  # read in TOA5 text file
        process_XML.main(rawdatx_config)    # make Excel file (do we want this?)
        
    def read_Hs_T(self):
        # df = pd.read_csv(r"../../../diss-data/Hs_T/Hm0-and-Tm02-and-fp-and-date-2016.csv")  # read Hs and T to a dataframe
        df = pd.read_csv(r"../../../diss-data/Race-Bank/2017-Race-Bank.csv")  # read Hs and T to a dataframe

        # reading entire Hs:T for all directions (unfiltered)
        
        return df

    def read_Hs_T_dir(self):
        # df = pd.read_csv(r"../../../diss-data/Hs_T/Hm0-and-Tm02-and-fp-and-date-2016.csv")  # read Hs and T to a dataframe
        df = pd.read_csv(r"../../../diss-data/Race-Bank/2017-Race-Bank.csv")  # read Hs and T to a dataframe
        
        
        dir_Hs_T_filtered = [None] * 4      # set up the list to be populated by direction filtered Hs:T
        dir_Hs_T_filtered[0] = df.loc[ (135 >= df['mdir']) &  (df['mdir'] > 45)]  # between NE and SE (i.e. E)
        dir_Hs_T_filtered[1] = df.loc[ (225 >= df['mdir']) &  (df['mdir']  > 135)]  # between SE and SW (i.e. S)
        dir_Hs_T_filtered[2] = df.loc[ (315 >= df['mdir']) &  (df['mdir']  > 225)]  # between SW and NW (i.e. W)
        dir_Hs_T_filtered[3] = df.loc[ (45 >= df['mdir']) |  (df['mdir']  > 315)]  # between NW and NE (i.e. N
        
        # also read direction, and return array of dataframes binned by direction
        
        return dir_Hs_T_filtered    
    #def Hs_T_histogram(self,hs_t_array):
        #plt.hist2d()
        