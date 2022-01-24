#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 18:59:17 2019

@author: xuefeng

Processing of S2S, S6N, S6S wells 
"""

import numpy as np

INCHES_TO_M = 0.0254
FEET_TO_M = 0.3048
S2_BW_Z = 423.3 # m
S6_BW_Z = 1390.40 # in feet  (platform elevation - Tyler's email 09/10/2020)
# coordinates are presented as (N,E,Z)
# absolute elevations 'z' -  are measured in 2020 by Tyler and Anne
# survey coordinates and depth to water measurements done during 2019 installation 

survey = {'KF42W': {'z': 1386.72, 'dtw': 0}, 
           'KF43W': {'z': 1387.07, 'dtw': 0},
           'KF45W': {'z': 1387.71, 'dtw': 0},           
           'S2S1': {'z': 1386.37, 'coords': [-15.91, -7.28, 0.65], 'dtw': 40-15.75}, 
           'S2S2': {'z': 1386.41, 'coords': [-8.76, -6.10, 0.67], 'dtw': 40-15.375}, 
           'S2S3': {'z': 1386.88, 'coords': [-1.9, 0.23, 0.81], 'dtw': 40-9.5 }, 
           
           'S6S1': {'z': 1388.21, 'coords': [-10.58, -3.58, 0.71], 'dtw':40-10.625 }, 
           'S6S2': {'z': 1388.05, 'coords': [3.37, 0.57, 0.97], 'dtw':50-10.15625 }, 
           'S6S3': {'z': 1388.18, 'coords': [13.62, 1.32, 0.70], 'dtw':40-10.875 }, 
           
           'S6N1': {'z': 1388.05, 'coords': [-2.90, -10.61, 0.47], 'dtw':40-12.15625  }, 
           'S6N2': {'z': 1388.23, 'coords': [-1.37, -2.30, 0.53], 'dtw':40-10  }, 
           'S6N3': {'z': 1388.14, 'coords': [-0.65, 3.73, 0.50], 'dtw':40-11.15625 },
           
           'S2_bogwell': {'z': 1388.78, 'coords':[40.69, -0.01, 1.40]},
           'S6_bogwell_S': {'z': S6_BW_Z, 'coords':[14.211, 0.002, 1.077]} ,
           'S6_bogwell_N': {'z': S6_BW_Z, 'coords':[-0.52, 28.02, 0.88]} ,
           }

# survey points from 2021 survey with Mariel and Xiating 
survey21_S2N = {'KF42W': {'coords': [-12.03, -6.94, 0.52]}, 
                'KF43W': {'coords': [-9.09, -5.95, 0.60]}, 
                'KF45W': {'coords': [1.72, -5.11, 0.79]},  
                'S2_bogwell': {'coords': [36.54, -0.01, 1.12]},
                'S2_nail': {'coords': [-22.50, -3.86, 1.16]}
                }
            
survey21_S2S = {'S2S1': {'coords': [-18.09, -11.34, 0.64]}, 
                'S2S2': {'coords': [-11.00, -9.61, 0.65]}, 
                'S2S3': {'coords': [-4.67, -2.83, 0.80]},
                'S2_bogwell': {'coords': [37.83, 0.02, 1.37]}
                }            

survey21_S6S = {'S6S1': {'coords': [12.90, 0.01, 0.49]}, 
                'S6S2': {'coords': [-1.66, -0.30, 0.76]}, 
                'S6S3': {'coords': [-11.73, 1.65, 0.48]},
                'S6_bogwell': {'coords': [-12.06, 3.13, 0.84]}
                }         

survey21_S6N = {'S6N1': {'coords': [-11.45, 2.72, 0.50]}, 
                'S6N2': {'coords': [-3.18, 1.11, 0.54]},  
                'S6N3': {'coords': [2.87, 0.35, 0.51]},
                'S6_bogwell': {'coords':[27.00, -0.01, 0.89]}, 
                'S6_nail': {'coords': [0.70, 3.82, 0.48]}
                }
                
print('2021 elevation surveys')
survey = survey21_S2N
well_names = ['KF42W', 'KF43W', 'KF45W']
for w in well_names: 
    print(w, np.round(S2_BW_Z + (survey[w]['coords'][2] - survey['S2_bogwell']['coords'][2] ), 3))
    
survey = survey21_S2S
well_names = ['S2S1', 'S2S2', 'S2S3' ]
for w in well_names: 
    print(w, np.round(S2_BW_Z + (survey[w]['coords'][2] - survey['S2_bogwell']['coords'][2] ), 3))
    
survey = survey21_S6S
well_names = ['S6S1', 'S6S2', 'S6S3']
for w in well_names: 
    print(w, np.round(S6_BW_Z*FEET_TO_M + (survey[w]['coords'][2] - survey['S6_bogwell']['coords'][2] ), 3))
    
survey = survey21_S6N
well_names = ['S6N1', 'S6N2', 'S6N3']
for w in well_names: 
    print(w, np.round(S6_BW_Z*FEET_TO_M + (survey[w]['coords'][2] - survey['S6_bogwell']['coords'][2] ), 3))
    

    
    
#%%
print('Elevations from 2020 surveys by Tyler ')
well_names = ['KF42W', 'KF43W', 'KF45W', 'S2S1', 'S2S2', 'S2S3', 'S6S1', 'S6S2', 'S6S3', 'S6N1', 'S6N2', 'S6N3']
for w in well_names: 
    print(w, ' elevation:', np.round(survey[w]['z']*FEET_TO_M, 3), ', dtw:', np.round(survey[w]['dtw']*INCHES_TO_M, 3))

print('Elevations fron 2019 surveys during installations')
# calculate 2019 S2S elevations from S2 Bogwell
well_names = ['S2S1', 'S2S2', 'S2S3']
for w in well_names: 
    print(w, np.round(survey['S2_bogwell']['z']*FEET_TO_M + (survey[w]['coords'][2] - survey['S2_bogwell']['coords'][2] ), 3))
    
# calculate 2019 S6S elevations from S2 Bogwell
well_names = ['S6S1', 'S6S2', 'S6S3']
for w in well_names: 
    print(w, np.round(survey['S6_bogwell_S']['z']*FEET_TO_M + (survey[w]['coords'][2] - survey['S6_bogwell_S']['coords'][2] ), 3))
    
# calculate 2019 S6N elevations from S2 Bogwell
well_names = ['S6N1', 'S6N2', 'S6N3']
for w in well_names: 
    print(w, np.round(survey['S6_bogwell_N']['z']*FEET_TO_M + (survey[w]['coords'][2] - survey['S6_bogwell_N']['coords'][2] ), 3))
   
    
#%%
''' plot x-y well positions '''

# # from Tyler's email 3/25/21 
# S2 bogwell:
# -93.46925, 47.5139
# platform elevation: 1388.76'

# S6 bogwell:
# -93.471154, 47.520183
# platform elevation: 1390.40'    

import geopy
import geopy.distance
from math import degrees, atan2
    
def gb(x, y, center_x, center_y):
    angle = degrees(atan2(y - center_y, x - center_x))
    # bearing1 = (angle + 360) % 360  1 
    bearing = (90 - angle) % 360 # North = 0
    dist = np.sqrt( (y - center_y)**2 + (x - center_x)**2)
    return dist, bearing

# Define starting point.
S2_bogwell = geopy.Point(latitude=47.5139, longitude=-93.46925)
S6_bogwell = geopy.Point(latitude=47.520183, longitude=-93.471154)



def find_well_coords(well_names, bog_name):
    bogwell_pt = survey[bog_name]['coords']
    for w in well_names: 
        
        bog_x, bog_y = bogwell_pt[1], bogwell_pt[0]
        well_x, well_y = survey[w]['coords'][1], survey[w]['coords'][1]
        dist, bearing = gb(well_x, well_y, bog_x, bog_y)
        
        start = S6_bogwell
        # Define a general distance object, initialized with a distance of 1 km.
        d = geopy.distance.distance(kilometers=dist/1000)
        
        # Use the `destination` method with a bearing of 0 degrees (which is north)
        # in order to go from point `start` 1 km to north.
        final = d.destination(point=start, bearing=bearing)
        print(w, np.round(final.longitude,8), np.round(final.latitude, 8))
    
print('Calculate absolute coordinates of wells')
well_names = ['S6S1', 'S6S2', 'S6S3']
bog_name = 'S6_bogwell_S'
find_well_coords(well_names, bog_name)

well_names = ['S6N1', 'S6N2', 'S6N3']
bog_name = 'S6_bogwell_N'
find_well_coords(well_names, bog_name)

well_names = ['S2S1', 'S2S2', 'S2S3']
bog_name = 'S2_bogwell'
find_well_coords(well_names, bog_name)
    
#%%    
# ''' S2-South ''' 
# # (N,E,Z) - in meters - Boglake well = 1388.78' = 423.3m
# BW2_coords = [40.69, -0.01, 1.40]
# S2S3_coords = [-1.9, 0.23, 0.81]
# S2S2_coords = [-8.76, -6.10, 0.67]
# S2S1_coords = [-15.91, -7.28, 0.65]

# # depth to water measurement (inches)
# S2S3_dtw = 40-9.5       # 11:15am, bog, 9/25/19
# S2S2_dtw = 40-15.375    # 11:21am, transition
# S2S1_dtw = 40-15.75     # 11:27am, lag

# ''' S6-South ''' 
# # (N,E,Z) - in meters - Boglake well = 1388.78' = 423.3m
# BW6_coords = [14.211, 0.002, 1.077]
# S6S3_coords = [13.62, 1.32, 0.70]
# S6S2_coords = [3.37, 0.57, 0.97]
# S6S1_coords = [-10.58, -3.58, 0.71]

# # depth to water measurement (inches)
# S6S1_dtw = 40-10.625    #10:01am, lag, 9/25/19
# S6S2_dtw = 50-10.15625  #10:08am, transition
# S6S3_dtw = 40-10.875    #10:18am, bog

# ''' S6-North ''' 
# BW6_coords = [-0.52, 28.02, 0.88]
# S6N3_coords = [-0.65, 3.73, 0.50]
# S6N2_coords = [-1.37, -2.30, 0.53]
# S6N1_coords = [-2.90, -10.61, 0.47]

# S6N1_dtw = 40-12.15625  # 3:34pm, lag
# S6N2_dtw = 40-10        # 3:43pm, transition
# S6N3_dtw = 40-11.15625  # 3:53pm, bog

# ''' Piezometer elevations in 2020 (feet) -- from Tyler's email 6/17/2020''' 
# KW42W_z = 1386.72
# KW43W_z = 1387.07
# KW45W_z = 1387.71
# S2S1_z = 1386.37
# S2S2_z = 1386.41
# S2S3_z = 1386.88
# S6N1_z = 1388.05
# S6N2_z = 1388.23
# S6N3_z = 1388.14
# S6S1_z = 1388.21
# S6S2_z = 1388.05
# S6S3_z = 1388.18
