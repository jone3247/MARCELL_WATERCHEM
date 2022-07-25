# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 11:37:15 2022

COPIED FROM process_timeseries3 WITH SOME WORKFLOW EDITS

@author: xuefeng
@author: marieljones

Designated workflow: 
    
    1. Manually identify the index for 'fixing' offset breakpoints
    2. Update breakpoint dictionary
    3. Automatically fix 
    4. loop through all wellnames and years
    
Still requiring processing: 
    1. Barometric pressure (15-min to 30-min intervales, available until 09/2020)
    2. Append new logger data and notes in 2021+22 (some available only to August due to frozen in)
    3. Elevation surveys in 2022
    
Possible issues
    KF series from 2020 still have issues: 43 is offset somehow...? -- fixed by adjusting initial calibration point. 
    S2S, 1-2 in 2019 has a weird shift towards November -- calibration point adjusted, need to double check. 
    S6 elevations are weird in 2020 is shifted, so is bogwell elevation 


Data sources: 
    BP Data -- Directly from Jake (MEF Hydrologist)
    Precipitation -- EDI edi.849.2 Marcell Experimental Forest 15-minute precipitation, 2010 - ongoing (Updated 2022-03-04)
    Bog Well Elevation -- EDI edi.562.2 Marcell Experimental Forest daily peatland water table elevation, 1961 - ongoing (Updated 2021-02-16)
    
MWJ - Updated 7/25/2022
Workflow structure has been changed to put all the processing in a loop so the adjustments are smoother

"""

#%% Import packages, define functions and dictionaries - not iteration specific DO NOT CHANGE

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import numba

''' FOLDER DIRECTORIES'''
folderpath = 'C:/Users/marie/Desktop/Feng Research/Data/Peatland Water Chemistry/Organized-20211102T181926Z-001/Organized/'

filepath = folderpath + 'consolidated_logger.xlsx'
notepath = folderpath + 'Raw from Anne/Well notes/Well_Piezo piezometers_210226.xlsx' #Dates got reconfigured in the new data file -- make sure that they transfer okay
precippath = folderpath + 'Atm_data/S2_precip2.xlsx'
BPpath = folderpath + 'Atm_data/S2bog_BP.xlsx'
bogwellpath = 'C:/Users/marie/Desktop/Publications/DOE MEF Water Table Data pub - edi.1126.1/MEF_daily_peatland_water_table.xlsx'

''' SUPPORTING FUNCTIONS AND DICTIONARIES '''
# =============================================================================
# Old Elevations, See new edits below
# elevs0 = {'KF42W': {'2018': 422.660, '2019':422.678, '2020':422.672}, 
#           'KF43W': {'2018': 422.782, '2019':422.810, '2020':422.779}, 
#           'KF45W': {'2018': 422.971, '2019':422.984, '2020':422.974},
#           
#           'S2S1': {'2019': 422.55, '2020':422.566 }, # 2019 can be calculated from S2 Bogwell 
#           'S2S2': {'2019': 422.57, '2020':422.578 }, 
#           'S2S3': {'2019': 422.71, '2020':422.721 }, 
#           
#           'S6S1': {'2019': 423.427, '2020':423.427}, # 2019 VALUES ARE REPLICATED FOR NOW DUE TO MATCH WITH BOGWELL DATA
#           'S6S2': {'2019': 423.687, '2020':423.687 }, # CHECK WHY LARGE DIFFERENCE -- LARGE STICK-UP HEIGHT
#           'S6S3': {'2019': 423.417, '2020':423.417 }, 
#           
#           'S6N1': {'2019': 423.384, '2020':423.384 }, # S6 bogwell elevation assumed to result in minimal difference between 2019 - 2020
#           'S6N2': {'2019': 423.444, '2020':423.444 }, 
#           'S6N3': {'2019': 423.414, '2020':423.414 }, 
#           } 
# =============================================================================

#Adjusted elevations to include 2021 -- still need to check the 2020 data (Xue has the surveying notes)
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

# spike detection and plotting options
THRESHOLD = 0.25        # for detecting peaks
PLOT_BAR = 10
OFFSET_THRESHOLD = 0.025 # m # for accounting for delays in calculating offset when patching
save = True
# plt.close('all')

#%% Patch Functions

###PLOT THE IDENTIFIED SPIKES
def patch_and_plot(signal):
    ###AUTOMATIC SPIKE DETECTION
    ispikes, _ = find_peaks(signal, prominence=THRESHOLD, distance=5)

    #Print the spikes -- for breakpoint updates
    print(ispikes)
    
    ###VISUALIZING PATCHING, CHECK WITH MANUAL MEASUREMENTS
    plt.figure(figsize=(8,3.5))
    plt.plot(signal)
    plt.plot(ispikes, signal[ispikes], 'x', color='green', label='automatic spikes detected')
    plt.plot(iwell_manual, signal[iwell_manual], 'x', color='red', label='timing of manual checks')
    for i, isp in enumerate(ispikes): 
        plt.annotate(str(i), (isp-2, signal[isp]-0.02))
        
    yesrain = np.where(precip_data2>0)[0]
    plt.vlines(yesrain, PLOT_BAR, PLOT_BAR + precip_data2.iloc[yesrain], color='lightgray')
    plt.hlines(PLOT_BAR, 0, len(precip_data2),  color='lightgrey')
    plt.legend()
    
    plt.title(wellname+', '+year)
    plt.tight_layout()
    plt.show()
    
###PATCHING WATER LEVEL SIGNAL AT BREAKPOINTS 
def patch_breakpoints(signal, breakpt_dict):
    # patch spikes before & after -- assume that after is offset to match exactly before
    signal_offset = signal.copy() # replicating water table series
    ibefore = breakpt_dict[wellname][year]['ibefore']
    iafter = breakpt_dict[wellname][year]['iafter']
    fill_option= breakpt_dict[wellname][year]['fill_opt']
    # include an option to just keep water table where it is at the end of the recovery & only interpolate the breakpoint
       
    # automatically iterate over spikes to calculate offset and fix
    if len(fill_option) == 0: 
        fill_option = len(ibefore)*[0] # this defaults to interpolating
        
    for i, (ibef, iaft) in enumerate(zip(ibefore, iafter)):
        
        # linearly interpolate between before and after
        if fill_option[i] == 0: 
            iinterp = np.arange(ibef, iaft+1)
            xp = [ibef, iaft]
            fp = [signal_offset[ibef], signal_offset[iaft]]
            signal_offset[iinterp] = np.interp(iinterp, xp, fp)
            
        # patch before and after by calculating offset 
        if fill_option[i] == 1:    
            offset = signal[iaft] - signal[ibef]
            signal_offset[ibef:iaft] = signal_offset[ibef]
            signal_offset[iaft:] = signal_offset[iaft:] - offset
    return signal_offset

##ATM DATA PROCESSING '''
@numba.jit(nopython=True)
def atm_data_matching(logger_time, BP_time, BP_data, precip_time, precip_data, bogwell_date, bogwell_wte):
    # find temperature, pressure, bogwell data closest to each well measurement 
    atm_arr = np.zeros((len(logger_time), 2))
    bog_arr = np.zeros(len(logger_time))
    for iw, logt in enumerate(logger_time): 
        ipressure = np.argmin(np.abs(BP_time - logt))
        iprecip = np.argmin(np.abs(precip_time - logt))
        ibog = np.argmin(np.abs(bogwell_date - logt))
        atm_arr[iw, 0] = BP_data[ipressure] #BP_data.iloc[ipressure]
        atm_arr[iw, 1] = precip_data[iprecip] #precip_data.iloc[iprecip]
        bog_arr[iw] = bogwell_wte[ibog]
    return atm_arr, bog_arr

#%% Set Well names and import specific data

''' IMPORT & EXPORT OPTIONS '''
# well and bog selections

# Loop through the available wells in the dictionary
for wellname in elevs0:
    
    #Assign the bog to the well
    if wellname in ['KF42W', 'KF43W', 'KF45W', 'S2S1', 'S2S2', 'S2S3']:
        bogname = 'S2'
    else:
        bogname = 'S6'
        
    #Loop through the years available for each well   
    for year in elevs0[wellname]:
        print(wellname, year, bogname)

        ''' DATA IMPORT '''
        # import well data
        sheet_name = wellname + '_' + year
        welldata = pd.read_excel(filepath, sheet_name=sheet_name, parse_dates=[['Date', 'Time']])
        logger_level = welldata['LEVEL'][:]
        logger_temp = welldata['TEMPERATURE'][:]
        logger_time = welldata['Date_Time'][:]
        
        # import notes
        notes = pd.read_excel(notepath, parse_dates=[['Date', 'Time']])
        note_time = notes['Date_Time']
        note_dtw = notes['DTW (m)']
        
        # import precip data
        ##### Updated through 2021 #####
        precip = pd.read_excel(precippath, sheet_name=year)
        precip_time = precip['TIMESTAMP'][:]
        precip_data = precip['South_PCP'][:]
        istart = abs(logger_time.iloc[0] - precip_time).argmin()
        iend = abs(logger_time.iloc[-1] - precip_time).argmin()
        # per 1/2 hourly data
        precip_time2 = precip_time[istart:iend][::2]
        precip_data2 = precip_data[istart:iend].groupby(precip_data[istart:iend].index // 2).sum() # summed to 1/2 hourly
        
        # import BP data    
        ##### Don't have BP data for 2021 or 2022 #####
        BP = pd.read_excel(BPpath, sheet_name=year)
        BP_data = BP['BPnorm_South'][:]  # kPa
        BP_time = BP['TIMESTAMP'][:]
        
        # import bogwell data 
        ##### Don't have 2021 or 2022 data for the bog well #####
        bogwell = pd.read_excel(bogwellpath, sheet_name=bogname)
        bogwell_date = bogwell['DATE']
        bogwell_wte = bogwell['WTE']
        
        
        ### NOTE DATA PROCESSING
        #find dtw notes closest to each well measurement
        # find index in notetime corresponding to given year and wellname
        
        note_wellyear = notes[(notes['Sampler#']==wellname) & (notes['Date_Time'].dt.year == int(year))]
        inote_wellyear = note_wellyear.index
          
        # find index of minimum distance between manual time and logger time                              
        iwell_manual = []
        for j in inote_wellyear: 
            iwell_manual.append(abs(note_time[j] - logger_time).argmin())  
            
        # create a column for notes in the same length as logger  
        notes_arr = np.zeros(len(logger_time))
        notes_arr[iwell_manual] = note_dtw[inote_wellyear]
    
        patch_and_plot(logger_level.values)
        patch_and_plot(logger_temp.values)

        ###MANUALLY EXAMINE BREAKPOINTS & ADD TO DICTIONARY
        #Script pauses for you to make adjustments to the breakpt_dicts file
        #input("Manually examine the breakpoints and add them to the breakpoints dictionary. Press any key to continue")

        ###PATCHING WATER LEVEL SIGNAL AT BREAKPOINTS 
        from breakpt_dicts import wtept_dict, temppt_dict
        logger_wte_offset = patch_breakpoints(logger_level.values, wtept_dict)
        logger_temp_offset = patch_breakpoints(logger_temp.values, temppt_dict)  

        #Type casting is converting to int so that the time series can be compared in the data matching
        atm_arr, bog_arr = atm_data_matching(np.array(logger_time).astype(int), 
                                             np.array(BP_time).astype(int), np.array(BP_data), 
                                             np.array(precip_time2).astype(int), np.array(precip_data2), 
                                             np.array(bogwell_date).astype(int), np.array(bogwell_wte))
        
        ###SHIFT TIME SERIES FOR LEVELS, TEMP, BP AT THE BEGINNING, TRUNCATE AT THE END '''
        jstart = wtept_dict[wellname][year]['istart'] # at 30-minute intervals
        jend = min(np.argmax(BP_time), np.argmax(logger_time))
        
        # extract time series in in array form 
        time_shifted            = pd.to_datetime(logger_time.dt.strftime("%Y-%m-%d %H:%M")).values[jstart:jend]
        logger_level_original   = logger_level[jstart:jend].values
        logger_level_shifted    = logger_wte_offset[jstart:jend]
        logger_temp_original    = logger_temp[jstart:jend].values
        logger_temp_shifted     = logger_temp_offset[jstart:jend]
        BP_data_shifted         = atm_arr[jstart:jend,0] * 1000                 # Pa, = kg/m-s2, check units: BP[Pa = kg/m-s2] * 1/g[s2/m] = [kg/m2] * 1/rho[m3/kg] = [m]
        precip_data_shifted     = atm_arr[jstart:jend,1]
        bogwell_wte_shifted     = bog_arr[jstart:jend]  
        notes_shifted           = notes_arr[jstart:jend]
        iwell_manual_shifted    = np.where(notes_shifted>0)[0]
        
        ###CONSOLIDATE INTO DATAFRAME ''' 
        df_all = pd.DataFrame({
                            'DateTime':     time_shifted, 
                            'LoggerLevel':  logger_level_shifted,        # m 
                            'LoggerTemp':   logger_temp_shifted,         # Celsius
                            'BP':           BP_data_shifted,             # Pa
                            'Precip':       precip_data_shifted,         # cm
                            'DTW':          notes_shifted,               # depth to water table (m)
                            'bogwell':      bogwell_wte_shifted,         # bogwell elevation (m)
                           })

        ###CALCULATE ABSOLUTE ELEVATION '''
        # constants and density functions
        g = 9.81                            # m/s2
        elev0 = elevs0[wellname][year]
        rho = lambda T: (0.99995 + (0.99995 - 0.99819)/(2-20)*T)*1000           # density of water, kg/m3
        rho2 =lambda T: (999.83952 + 16.945176*T - 7.9870401*10**(-3)*T**2
                         - 46.170461*10**(-6)*T**3 + 105.56302*10**(-9)*T**4
                         - 280.54253*10**(-12)*T**5)/(1 + 16.89785*10**(-3)*T)  # density of water, kg/m3, Steve's option
        
        # calculate correction factors for pressure, dtw, and levels
        icalib = np.where(notes_shifted>0)[0][0]        # index of first not nan measurement in the logger timestamp
        dtw0 = notes_shifted[icalib]                    # m, first calibration measurement
        BP0 = BP_data_shifted[icalib]                   # Pa, barometric pressure at calibration, Pa = kg/m-s2
        level0 = logger_level_shifted[icalib]           # m, water level logged at calibration
        
        # equation used to calcualted elevation
        wt_elev = (logger_level_shifted - level0) + (elev0 - dtw0) - (BP_data_shifted - BP0) / (g * rho2(logger_temp_shifted))

        ''' VISUALIZE TO SEE EFFECT OF PATCHING, AND COMPARE WITH BOGWELL DATA '''
        plt.figure(figsize=(8,6))
        
        plt.subplot(211) 
        plt.plot(logger_level_original, label='original')
        plt.plot(logger_level_shifted, label='patched')
        plt.plot(iwell_manual_shifted, logger_level_original[iwell_manual_shifted], 'x', ms=5, color='red', label='manual checkpoints')
        plt.plot(iwell_manual_shifted, logger_level_shifted[iwell_manual_shifted], 'x', ms=5, color='red')
        plt.legend()
        plt.title(wellname+', '+year)
        
        plt.subplot(212)
        # plot rain  
        plt.plot(time_shifted, elev0-1.0+precip_data_shifted, color='lightgray')
        # plot elevations
        plt.plot(time_shifted, bogwell_wte_shifted, 'o', ms=0.5, color='lightgray')
        plt.plot(time_shifted, wt_elev)
        plt.plot(note_time[inote_wellyear], elev0 - note_dtw[inote_wellyear], 'x', ms=5, mew=2, color='brown', label='calibration points')
        plt.legend()
        
        plt.gcf().autofmt_xdate()
        
        plt.figure(figsize=(8,3.5))
        plt.plot(logger_temp_original, label='original')
        plt.plot(logger_temp_shifted, label='patched')
        plt.plot(iwell_manual_shifted, logger_level_original[iwell_manual_shifted], 'x', ms=5, color='red', label='manual checkpoints')
        plt.plot(iwell_manual_shifted, logger_level_shifted[iwell_manual_shifted], 'x', ms=5, color='red')
        plt.legend()
        plt.title(wellname+', '+year)
        plt.show()
        
        ''' WRITE TO EXCEL '''
        # save = True
        if save: 
            from openpyxl import load_workbook
            def save_to_excel(df, path, sheet_name): 
                book = load_workbook(path)
                writer = pd.ExcelWriter(path, engine = 'openpyxl')
                writer.book = book
                try:
                    book.remove(book[sheet_name])
                except: 
                    print('sheet does not exist - new sheet added')
                else: 
                    print('replace old sheet')
                finally:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                writer.save()
                writer.close()
            
            df_all['well_elev'] = wt_elev
            save_to_excel(df_all, path = 'C:/Users/marie/Desktop/Publications/DOE MEF Water Table Data pub - edi.1126.1/01_filled_data.xlsx',  sheet_name = wellname + ', ' + year)
        
        # #print(min(logger_temp_original))
        # #print(min(logger_temp_shifted))