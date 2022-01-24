#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 11:42:19 2021

@author: xuefeng

Designated workflow: 
    
    1. First, manually identify the index for 'fixing' offset points
    2. Update index dictionary
    3. Automatically fix 
    
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

''' FOLDER DIRECTORIES'''
plt.close('all')
folderpath = '/Users/xuefeng/Desktop/Peatland/Well_data/Organized/'
filepath = folderpath + 'consolidated.xlsx'
notepath = folderpath + 'Raw from Anne/Well notes/Well_Piezo piezometers.xlsx'
precippath = folderpath + 'Atm_data/S2_precip.xlsx'
BPpath = folderpath + 'Atm_data/S2bog_BP.xlsx'
bogwellpath = '/Users/xuefeng/Desktop/Peatland/Well_data/edi.562.1/MEF_daily_peatland_water_table.xlsx'

def save_to_excel(df, path, sheet_name): 
    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine = 'openpyxl')
    writer.book = book
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
    writer.close()

elevs0 = {'KF42W': {'2018': 422.660, '2019':422.678, '2020':422.672}, 
          'KF43W': {'2018': 422.782, '2019':422.810, '2020':422.779}, 
          'KF45W': {'2018': 422.971, '2019':422.984, '2020':422.974},
          
          'S2S1': {'2019': 422.55, '2020':422.566 }, # 2019 can be calculated from S2 Bogwell 
          'S2S2': {'2019': 422.57, '2020':422.578 }, 
          'S2S3': {'2019': 422.71, '2020':422.721 }, 
          
          'S6S1': {'2019': 423.122, '2020':423.126 }, # values replicated from 2020 until 2019 is updated
          'S6S2': {'2019': 423.382, '2020':423.078 }, # CHECK WHY LARGE DIFFERENCE -- LARGE STICK-UP HEIGHT
          'S6S3': {'2019': 423.112, '2020':423.117 }, 
          
          'S6N1': {'2019': 423.079, '2020':423.078 }, # S6 bogwell elevation assumed to result in minimal difference between 2019 - 2020
          'S6N2': {'2019': 423.139, '2020':423.133 }, 
          'S6N3': {'2019': 423.109, '2020':423.105 }, 
          } 

dtws0 = {'KF42W': {'2018': 0.84, '2019':0.762}, 
        'KF43W': {'2018': 0.961, '2019':0.883}, 
        'KF45W': {'2018': 1.113, '2019':1.067}, 
        
        'S2S1': {'2019': 0.616, '2020':np.nan}, # 2020 data needs to come from Anne
        'S2S2': {'2019': 0.625, '2020':np.nan}, 
        'S2S3': {'2019': 0.775, '2020':np.nan}, 
        
        'S6S1': {'2019': 0.746, '2020':np.nan}, 
        'S6S2': {'2019': 1.012, '2020':np.nan}, 
        'S6S3': {'2019': 0.740, '2020':np.nan}, 
        
        'S6N1': {'2019': 0.707, '2020':np.nan}, 
        'S6N2': {'2019': 0.762, '2020':np.nan}, 
        'S6N3': {'2019': 0.733, '2020':np.nan}, 
        }


''' OPTIONS '''
# for wellname in ['S2S1', 'S2S2', 'S2S3', 'S6S1', 'S6S2', 'S6S3', 'S6N1', 'S6N2', 'S6N3']:
#     for year in ['2019']:
        # year = '2019'
        # wellname = 'KF43W' # KF42W, KF43W, KF45W, S2S(1-3), S6S(1-3), S6N(1-3)

save = False
wellname = 'S2S1'
year = '2019'
bogname = 'S2'
print(wellname, year)

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
precip = pd.read_excel(precippath, sheet_name=year, parse_dates={'Date_Time':['Year', 'YearDay', 'Hours', 'Minutes']} , 
                    date_parser=lambda x: dt.datetime.strptime(x, '%Y %j %H %M'))
precip_time = precip['Date_Time'][:]
precip_data = precip['ReportPCP'][:]
istart = abs(logger_time.iloc[0] - precip_time).argmin()
iend = abs(logger_time.iloc[-1] - precip_time).argmin()
# per 1/2 hourly data
precip_time2 = precip_time[istart:iend][::2]
precip_data2 = precip_data[istart:iend].groupby(precip_data[istart:iend].index // 2).sum() # summed to 1/2 hourly

# import BP data 
if year =='2018':   
    BP = pd.read_excel(BPpath, sheet_name=year, parse_dates={'Date_Time':['Year', 'DoY', 'Hours', 'Minutes']}, 
                        date_parser = lambda x: dt.datetime.strptime(x, '%Y %j %H %M'))
if year=='2019': BP = pd.read_excel(BPpath, sheet_name=year, parse_date=[['Date_Time']])
BP_data = BP['BP_norm'][:]  # kPa
BP_time = BP['Date_Time'][:]

# import bogwell data 
bogwell = pd.read_excel(bogwellpath, sheet_name=bogname)
bogwell_date = bogwell['DATE']
bogwell_wte = bogwell['WTE']

''' DATA PROCESSING '''

''' find temperature, pressure, bogwell data closest to each well measurement '''
atm_arr = np.zeros((len(logger_time), 2))
bog_arr = np.zeros(len(logger_time))
for iw, logt in enumerate(logger_time): 
    ipressure = np.argmin(abs(BP_time - logt))
    iprecip = np.argmin(abs(precip_time2 - logt))
    ibog = np.argmin(abs(bogwell_date - logt))
    atm_arr[iw, 0] = BP_data.iloc[ipressure]
    atm_arr[iw, 1] = precip_data2.iloc[iprecip]
    bog_arr[iw] = bogwell_wte[ibog]

''' find dtw notes closest to each well measurement '''
# find index in notetime corresponding to given year and wellname
note_wellyear = notes[(notes['Sampler#']==wellname) & (notes['Date_Time'].dt.year == int(year))]
inote_wellyear = note_wellyear.index
  
# find index of minimum distance between manual time and logger time                              
iwell_manual = []
for j in inote_wellyear: 
    iwell_manual.append(abs(note_time[j] - logger_time).argmin())  
    
# create a column for notes in the same length as logger  
notes_arr = np.zeros(len(logger_time))
for iw, im in zip(iwell_manual, inote_wellyear): 
    notes_arr[iw] = note_dtw[im]

''' CONSOLIDATE INTO DATAFRAME ''' 
df_all = pd.DataFrame({
                    'DateTime': pd.to_datetime(logger_time.dt.strftime("%Y-%m-%d %H:%M").values), 
                    'LoggerLevel': logger_level,    # m 
                    'LoggerTemp': logger_temp,      # Celsius
                    'BP': atm_arr[:,0],             # kPa
                    'Precip': atm_arr[:,1],         # ? 
                    'DTW': notes_arr,               # depth to water table (m)
                    'bogwell': bog_arr,             # bogwell elevation (m)
                   })

''' CALCULATE ELEVATION '''
# elev = (logger_level - logger_level0) +  (elev0 - dtw0) - (BP-BP0) / (g*rho(temp)) 

# get rid of some initial values in the time series for levels, temp, BP
jstart = 1 # at 30-minute intervals
jend = min(np.argmax(BP_time), np.argmax(logger_time))
# extract in array form 
time_shifted = df_all['DateTime'][jstart:jend].values
logger_level_shifted = df_all['LoggerLevel'][jstart:jend].values
logger_temp_shifted = df_all['LoggerTemp'][jstart:jend].values
BP_data_shifted = df_all['BP'][jstart:jend].values * 1000         # Pa, = kg/m-s2
bogwell_wte_shifted = df_all['bogwell'][jstart:jend].values
# BP[Pa = kg/m-s2] * 1/g[s2/m] = [kg/m2] * 1/rho[m3/kg] = [m]

# constants and density functions
g = 9.81                            # m/s2
elev0 = elevs0[wellname][year]
rho = lambda T: (0.99995 + (0.99995 - 0.99819)/(2-20)*T)*1000           # density of water, kg/m3
rho2 =lambda T: (999.83952 + 16.945176*T - 7.9870401*10**(-3)*T**2
                 - 46.170461*10**(-6)*T**3 + 105.56302*10**(-9)*T**4
                 - 280.54253*10**(-12)*T**5)/(1 + 16.89785*10**(-3)*T)  # density of water, kg/m3, Steve's option

# correction factors for pressure, dtw, and levels
inote_notnan = np.where(note_wellyear['DTW (m)']>0)[0][0] # index of first not nan measurement in manual notes
icalib = iwell_manual[inote_notnan]      # index of first not nan measurement in the logger timestamp
dtw0 = notes_arr[icalib]                # m, first calibration measurement
BP0 = BP_data_shifted[icalib]      # Pa, barometric pressure at calibration, Pa = kg/m-s2
level0 = logger_level_shifted[icalib]  # m, water level logged at calibration

''' Corrections from Steve's work : 
    (1) align the pressure corrections with time of logger corrections
    (2) get BP to start at start of measurements '''
wt_elev = (logger_level_shifted - level0) + (elev0 - dtw0) - (BP_data_shifted - BP0) / (g * rho2(logger_temp_shifted))

''' VISUALIZE AND COMPARE WITH BOGWELL DATA '''
plt.figure()
plt.plot(time_shifted, bogwell_wte_shifted, 'o', ms=0.5, color='lightgray')
plt.plot(time_shifted, wt_elev)
plt.plot(note_time[inote_wellyear], elev0 - note_dtw[inote_wellyear], 'x', ms=5, mew=2, color='red')
plt.gcf().autofmt_xdate()
plt.show()

''' AUTOMATIC SPIKE DETECTION '''
from scipy.signal import find_peaks
THRESHOLD = 0.25        # for detecting peaks
PLOT_BAR = 10
OFFSET_THRESHOLD = 0.025 # m # for accounting for delays in calculating offset when patching

signal = logger_level_shifted
ispikes, _ = find_peaks(signal, prominence=THRESHOLD, distance=5)

''' PATCHING WATER LEVEL SIGNAL ''' 
# patch spikes before & after -- assume that after is offset to match exactly before
signal_offset = signal.copy() # replicating water table series
# to designate distance of the ibefore index before spike
prior_indices = np.array([0]*len(ispikes)) # defaults to some index value (0) before spike

# iterate over spikes to fix
for i, (k, ip) in enumerate(zip(ispikes, prior_indices)):
    ibefore = k-ip
    # to account for delayed return to pre conditions, the "after" index is designated as when wt difference returns to below threshold
    # calculate the difference between 12 points after the spike and before the spike, take 1st instance of rebound
    try: # defaults to where wt rebounded within threshold difference before/after -- may experience delays in the "bounce"
        ioffset = np.where(abs( signal[(ibefore+1):(ibefore+12)] - signal[ibefore] ) < OFFSET_THRESHOLD)[0][0] 
    except IndexError: 
        # signal never rebounds within threshold difference 
        # take position of maximum difference between before and after
        ioffset = np.argmin(abs( signal[(ibefore+1):(ibefore+4)] - signal[ibefore] ))
    
    iafter = (ibefore + 1) + ioffset
    offset = signal[iafter] - signal[ibefore]
    # correct for spikes at designated indices
    signal_offset[ibefore:iafter] = signal_offset[ibefore]
    signal_offset[iafter:] = signal_offset[iafter:] - offset
    
# fix spike at beginning of time series
try: 
    iinit = np.where(abs( signal_offset[0] - signal_offset[:10] ) > OFFSET_THRESHOLD)[0][0] 
except IndexError: 
    iinit = 0
signal_offset1 = signal_offset[iinit:]
        

'''VISUALIZING PATCHING, CHECK WITH MANUAL MEASUREMENTS'''
plt.figure(figsize=(8,7))

plt.subplot(211)
plt.plot(signal)
plt.plot(ispikes, signal[ispikes], 'x', label='automatic spikes detected')
plt.plot(iwell_manual, signal[iwell_manual], 'x', color='red', label='timing of manual measurements')
for i, isp in enumerate(ispikes): 
    plt.annotate(str(i), (isp-2, signal[isp]-0.02))
    
yesrain = np.where(precip_data2>0)[0]
plt.vlines(yesrain, PLOT_BAR, PLOT_BAR + precip_data2.iloc[yesrain], color='lightgray')
plt.hlines(PLOT_BAR, 0, len(precip_data2),  color='lightgrey')
plt.legend()

# visualize offseted water table series
plt.subplot(212)
plt.plot(signal[iinit:], label='original')
plt.plot(signal_offset1, label='patched')
plt.legend()

plt.suptitle(wellname+', '+year)
plt.tight_layout()
plt.show()

''' RECALCULATE WT_ELEVATION '''
wt_elev_offset = (signal_offset - level0) + (elev0 - dtw0) - (BP_data_shifted - BP0) / (g * rho2(logger_temp_shifted))

plt.figure()
plt.plot(time_shifted, bogwell_wte_shifted, 'o', ms=0.5, color='lightgray')
plt.plot(time_shifted, wt_elev_offset)
plt.plot(note_time[inote_wellyear], elev0 - note_dtw[inote_wellyear], 'x', ms=5, mew=2, color='red')
plt.gcf().autofmt_xdate()
plt.show()

''' WRITE TO EXCEL '''
if save: 
    from openpyxl import load_workbook
    save_to_excel(df_all, path=folderpath + 'welldata_consolidated.xlsx',  sheet_name=wellname+', '+year)






