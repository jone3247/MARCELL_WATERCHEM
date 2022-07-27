# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 10:53:59 2022

@author: marieljones

This scipt takes in the manually filled data files and makes a final plot of 
each year of well elevations and then merges the sheets of the excel file so 
that it is in .csv form. A column for watershed, year, and well name is added. 

Workflow:
    1. Import the manually filled data and the well elevations from the process_timeseries codes.
    2. Loop through the dictionary and first plot each well/year timeseries for a final check
    3. Create an indicator column with the well name, the watershed label, and the year
    4. Concat to into dataframe
    

"""

#%% Import packages, define functions and dictionaries

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

''' DATA IMPORT '''
filepath = 'C:/Users/marie/Desktop/Publications/DOE MEF Water Table Data pub - edi.1126.1/edi.1126.1/manual_na_filled_data.xlsx'

elevs0 = {'KF42W': {'2018': 422.66, '2019':422.68, '2020':422.67}, # '2021':422.69}, 
          'KF43W': {'2018': 422.78, '2019':422.81, '2020':422.78}, # '2021':422.77}, 
          'KF45W': {'2018': 422.97, '2019':422.98, '2020':422.97}, # '2021':422.96},
          
          'S2S1': {'2019': 422.54, '2020':422.57}, # '2021':422.56}, 
          'S2S2': {'2019': 422.56, '2020':422.58}, # '2021':422.57}, 
          'S2S3': {'2019': 422.70, '2020':422.72}, # '2021':422.72}, 
          
          'S6S1': {'2019': 423.42, '2020':423.43}, # '2021': 423.44}, 
          'S6S2': {'2019': 423.68, '2020':423.70}, # '2021': 423.71}, 
          'S6S3': {'2019': 423.41, '2020':423.42}, # '2021': 423.43}, 
          
          'S6N1': {'2019': 423.38, '2020':423.40}, # '2021': 423.41}, 
          'S6N2': {'2019': 423.44, '2020':423.44}, # '2021': 423.44}, 
          'S6N3': {'2019': 423.41, '2020':423.40}, # '2021': 423.40}, 
          } 

''' DATAFRAME FOR CONCAT AND EXPORT'''
df_all = pd.DataFrame(columns = {
                    'DateTime', 
                    'LoggerLevel',     # m 
                    'LoggerTemp',      # Celsius
                    'BP',              # Pa
                    'Precip',          # cm
                    'DTW',             # depth to water table (m)
                    'bogwell',         # bogwell elevation (m)
                    'well_elev',       # well elevation (m)
                    'well_name', 
                    'watershed', 
                    'year'
                   })

#%%
# Loop through the available wells in the dictionary
for wellname in elevs0:
    
    #Assign the bog to the well
    if wellname in ['KF42W', 'KF43W', 'KF45W', 'S2S1', 'S2S2', 'S2S3']:
        bogname = 'S2'
    else:
        bogname = 'S6'
        
    #Loop through the years available for each well   
    for year in elevs0[wellname]:
        #Import sheet with year and well
        sheet_name = wellname + ', ' + year
        welldata = pd.read_excel(filepath, sheet_name = sheet_name,
                                 parse_dates = ['DateTime'], 
                                 na_values = -9999)
        
        #Pull out time, precip, and water table data
        time = welldata['DateTime']
        precip = welldata['Precip']
        wt_elev = welldata['well_elev']
        #Elevation (for plotting)
        elev0 = elevs0[wellname][year]

        ''' VISUALIZE TO SEE EFFECT OF PATCHING, FILLING, AND COMPARE WITH BOGWELL DATA '''
        plt.figure(figsize = (6,4))
        # plot rain  
        plt.plot(time, elev0 -1.0 + precip, color='lightgray')
        # plot elevations
        plt.plot(time, wt_elev)
        # fix dates along x axis
        plt.gcf().autofmt_xdate()
        plt.title(wellname+', '+year)
        
        ''' ADD INDICATOR COLUMNS '''
        welldata['well_name'] = wellname
        welldata['watershed'] = bogname
        welldata['year'] = year
        
        ''' CONCAT '''
        df_all = pd.concat([df_all, welldata])

#%%

''' EXPORT '''
pd.to_csv(df_all, path = 'C:/Users/marie/Desktop/Publications/DOE MEF Water Table Data pub - edi.1126.1/edi.1126.1/final_data.csv')

