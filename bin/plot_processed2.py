#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 11:11:47 2021

@author: xuefeng
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

folderpath = '/Users/xuefeng/Desktop/Peatland/Well_data/Organized/'
filepath = folderpath + 'processed_wte_atm.xlsx'

bogname = 'S2N'
# in order of lagg, transition, bog
wells_dict = {'S2N':['KF42W', 'KF43W', 'KF45W'], 
              'S2S':['S2S1','S2S2','S2S3'], 
              'S6S':['S6S1','S6S2','S6S3'],
              'S6N':['S6N1','S6N2','S6N3']}
wells = wells_dict[bogname]


def import_data(bog, year):
    wellname = wells[0]; print(wellname, year)
    sheet_name = wellname + ', ' + year
    welldata = pd.read_excel(filepath, sheet_name=sheet_name)
    
    well_df = welldata[['DateTime', 'well_elev', 'Precip', 'bogwell', 'LoggerTemp']]
    # rename the columes so that it doesn't conflict with other well data names
    well_df = well_df.rename(columns={'well_elev':'elevs_'+wellname, 'LoggerTemp':'temp_'+wellname})
    # need to round time to nearest 30 min intervals
    well_df['DateTime']=well_df['DateTime'].dt.round('30min') 
    
    # import subsequently from the rest of the wells
    for wellname in wells[1:]: 
        print(wellname)
        sheet_name = wellname + ', ' + year
        welldata = pd.read_excel(filepath, sheet_name=sheet_name)
        well_df2 = welldata[['DateTime', 'well_elev', 'LoggerTemp']]
        well_df2 = well_df2.rename(columns={'well_elev':'elevs_'+wellname, 'LoggerTemp':'temp_'+wellname})
        well_df2['DateTime']=well_df2['DateTime'].dt.round('30min') 
        well_df = well_df.merge(well_df2, on='DateTime', how='inner')
    return well_df


wells18 = import_data(bogname, '2018')
wells19 = import_data(bogname, '2019')
wells20 = import_data(bogname, '2020')
well_df = pd.concat([wells18, wells19, wells20])
# well_df = pd.concat([wells19, wells20])

#%%
P0 = 422.2 # offset assigned to plotting rainfall, 412.7 for S2
ms = 0.5
plt.figure(figsize=(8,5))
plt.subplot(211) # plot absolute well elevations
plt.plot(well_df['DateTime'], P0 + 0.1*well_df['Precip'],  color='lightgray')
plt.plot(well_df['DateTime'], well_df['bogwell'], 'o', color='lightgray', label='bogwell')
for wellname in wells:
    plt.plot(well_df['DateTime'], well_df['elevs_'+wellname], 'o', ms=ms, label=wellname)
plt.legend()
plt.ylabel('Well elevations (m)')
plt.subplot(212) # plot wte gradients
plt.plot(well_df['DateTime'], np.zeros(len(well_df['DateTime'])), color='lightgrey')
plt.plot(well_df['DateTime'], well_df['elevs_'+wells[-1]] - well_df['elevs_'+wells[1]], 'o', ms=ms, color='pink', label='bog - transition', alpha=0.5)
plt.plot(well_df['DateTime'], well_df['elevs_'+wells[-1]] - well_df['elevs_'+wells[0]], 'o', ms=ms, color='brown', label='bog - lagg')
plt.legend()
plt.ylabel('Head gradient (m)')
plt.tight_layout()

plt.figure(figsize=(8,3))
for wellname in wells:
    plt.plot(well_df['DateTime'], well_df['temp_'+wellname], 'o', ms=ms, label=wellname)
plt.legend()
plt.show()

#%% Analysis 

plt.figure()
for well_df in [wells18, wells19, wells20]:
    plt.plot(well_df['elevs_'+wells[-1]], well_df['elevs_'+wells[-1]] - well_df['elevs_'+wells[0]], 'o', ms=2, alpha=0.5)
plt.show()




