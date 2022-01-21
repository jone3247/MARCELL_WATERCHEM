#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 11:56:52 2020

@author: xuefeng

TODO: 
- Get precipitation and BP data for 2020
- Elevation adjustments for S2S, S6S, S6N wells
- Temperature adjustments for calculating elevation? 
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import datetime as dt

''' FOLDER DIRECTORIES'''
plt.close('all')
folderpath = '/Users/xuefeng/Desktop/Peatland/Well_data/Organized/'
filepath = folderpath + 'consolidated.xlsx'
notepath = folderpath + 'Raw from Anne/Well notes/Well_Piezo piezometers.xlsx'
precippath = folderpath + 'Atm_data/S2_precip.xlsx'
BPpath = folderpath + 'Atm_data/S2bog_BP.xlsx'

'''PARAMETERS'''
# parameters for spike detection and patching
PROMINENCE_THRESHOLD = 0.05         # for detecting peaks
OFFSET_THRESHOLD = 0.025 # m        # for accounting for delays in calculating offset when patching
g = 9.80665 # acceleration due to gravity
rho = lambda T: 0.99995 + (0.99995 - 0.99819)/(2-20)*T  # density of water

# elevation parameters 
RHO = 0.999         # density (temperature adjustments available, but not used here)
G = 9.80665         # acceleration due to gravity
PSCALE = 0.101972   # convert between kPa and m, according to Solinst

# plotting parameters 
BAR = 9.5           # values where rainfall bars originate
BAR_ELEV = 421.0    # for when the scales are in terms of elevation

''' OPTIONS '''
year = '2018'
wellname = 'KF45W' # KF42W, KF43W, KF45W, S2S(1-3), S6S(1-3), S6N(1-3)
manual_patch_on = True # run first without to identify the spikes that needs repairing, then run with manual_patch on
manual_prior_index = None #[2]  # to designate manually distance of the ibefore index before spike
manual_post_index = None #[1]  # the "after" index is designated as when wt difference returns to before threshold
        # calculate the difference between 12 points after the spike and before the spike, take 1st instance of rebound

elevation_adjustment = True
save_to_excel = False

''' DICTIONARIES '''
manual_patch_indices = {'KF42W': {'2018': [5,6,8,10,12,22,32],  '2019':[40]},
                        'KF43W': {'2018': [4,5,7,9],            '2019':[44]},
                        'KF45W': {'2018': [5,6,7,9,11,18,36],   '2019':[57]}, # [2][1] for prior/post index (2019)
                        
                        'S2S1': {'2019': [12]},
                        'S2S2': {'2019': [14]},
                        'S2S3': {'2019': [10]}, # [2] for prior index
                        
                        'S6S1': {'2019': [12]}, # [3] for prior index
                        'S6S2': {'2019': [10]}, # [4][1] for prior/post index
                        'S6S3': {'2019': [15]}, # [3][1] for prior/post index
                        
                        'S6N1': {'2019': []}, 
                        'S6N2': {'2019': []}, 
                        'S6N3': {'2019': []}, 
                        }

# 2018 (KW): from Tyler's email 42W 1386.68’, 43W 1387.08’, 45W 1387.70’ (m)
# 2019 (KW): from Tyler's email of nail elevation, subtract from it survey elevations; elev_nail + (np.array(dz) - z_nail)
# 2019 (S2S, S6S, S6N): relative elevation and dtw, from initial survey during installation -- Rachel notebook
# 2020 (KW, S2S, S6S, S6N): absolute elevation from Tyler's follow-up survey -- Tyler email 

# Still need to request precipitation and BP for 2020. 
# Then, plot all wells on the same gradient together 

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


''' DATA IMPORT '''
# import well data
sheet_name = wellname + '_' + year
welldata = pd.read_excel(filepath, sheet_name=sheet_name, parse_dates=[['Date', 'Time']])
wt = welldata['LEVEL'][:]
temp = welldata['TEMPERATURE'][:]
welltime = welldata['Date_Time'][:]

# import notes
notes = pd.read_excel(notepath, parse_dates=[['Date', 'Time']])
imanual = np.where(notes['Sampler#']==wellname)[0]
notetime = notes['Date_Time']
dtw = notes['DTW (m)']

# import precip data
precip = pd.read_excel(precippath, sheet_name=year, parse_dates={'Date_Time':['Year', 'YearDay', 'Hours', 'Minutes']} , 
                    date_parser=lambda x: dt.datetime.strptime(x, '%Y %j %H %M'))
preciptime = precip['Date_Time'][:]
precipdata = precip['ReportPCP'][:]
istart = abs(welltime.iloc[0] - preciptime).argmin()
iend = abs(welltime.iloc[-1] - preciptime).argmin()
precip2 = precipdata[istart:iend].groupby(precipdata[istart:iend].index // 2).sum() # summed to 1/2 hourly

# import BP data 
if year =='2018':   
    BP = pd.read_excel(BPpath, sheet_name=year, parse_dates={'Date_Time':['Year', 'DoY', 'Hours', 'Minutes']}, 
                        date_parser = lambda x: dt.datetime.strptime(x, '%Y %j %H %M'))
if year=='2019': BP = pd.read_excel(BPpath, sheet_name=year, parse_date=[['Date_Time']])
pressure = BP['BP_norm'][:]  # kPa
BPtime = BP['Date_Time'][:]
P0 = pressure[0]


''' SPIKE DETECTION '''
# find timing of closest manual measurements during given year
df = notetime[imanual].dt.year == int(year)
icompare = df[df==True].index                                   # find index in notetime corresponding to given year
iwellmanual = []
for j in icompare: 
    iwellmanual.append(abs(notetime[j] - welltime).argmin())    # find index of minimum distance between manual time and well time

# find spikes
ispikes, _ = find_peaks(-wt, prominence=PROMINENCE_THRESHOLD)


''' INITIAL VISUALIZATION ''' 
# visualize data with spikes, check with timing of manual measurements 
plt.figure(figsize=(8,7))

plt.subplot(211)
plt.plot(wt)
plt.plot(iwellmanual, wt[iwellmanual], 'o', label='timing of manual measurements')
plt.plot(ispikes, wt[ispikes], 'x', label='automatic spikes detected')
for i, isp in enumerate(ispikes): 
    plt.annotate(str(i), (isp-2, wt[isp]-0.02))
plt.legend()

yesrain = np.where(precip2>0)[0]
plt.vlines(yesrain, BAR, BAR+precip2.iloc[yesrain])
plt.hlines(BAR, 0, len(precip2))


''' PATCHING AND ELEVATION ADJUSTMENTS ''' 
# patch spikes before & after -- assume that after is offset to match exactly before
if manual_patch_on: 
    ispk = ispikes[manual_patch_indices[wellname][year]]
    wt_offset = wt.copy() # replicating water table series
    
    # to designate manually distance of the ibefore index before spike
    if manual_prior_index is not None: 
        prior_indices = np.array( manual_prior_index )
    else: 
        prior_indices = np.array([1]*len(ispk)) # defaults to 1 before spike

    # iterate over spikes to fix
    for i, (k, ip) in enumerate(zip(ispk, prior_indices)):
        ibefore = k-ip
        # to account for delayed return to pre conditions, the "after" index is designated as when wt difference returns to below threshold
        # calculate the difference between 12 points after the spike and before the spike, take 1st instance of rebound
        if manual_post_index is not None: 
            iafter = ibefore + manual_post_index[i]
        else: 
            try: # defaults to where wt rebounded within threshold difference before/after
                ioffset = np.where(abs( wt[(ibefore+1):(ibefore+12)] - wt[ibefore] ) < OFFSET_THRESHOLD)[0][0] 
            except IndexError: 
                # never rebounds within threshold difference - take position of maximum difference between before and after
                ioffset = np.argmin(abs( wt[(ibefore+1):(ibefore+4)] - wt[ibefore] ))
            
            iafter = (ibefore+1) + ioffset
            offset = wt[iafter] - wt[ibefore]
        
        # correct for spikes at designated indices
        wt_offset[ibefore:iafter] = wt_offset[ibefore]
        wt_offset[iafter:] = wt_offset[iafter:] - offset
    
    # fix spike at beginning of time series
    try: 
        iinit = np.where(abs( wt_offset[0] - wt_offset[:10] ) > OFFSET_THRESHOLD)[0][0] 
    except IndexError: 
        iinit = 0
        
    wt_offset0 = wt_offset[iinit:]
    well_time0 = welltime[iinit:]
    precip2 = precip2[iinit:]
    temp0 = temp[iinit:]
            
    # visualize offseted water table series
    plt.subplot(212)
    plt.plot(wt[iinit:], label='original')
    plt.plot(wt_offset0, label='patched')
    plt.legend()

plt.suptitle(wellname+', '+year)
plt.tight_layout()

if elevation_adjustment: 
    # convert to elevation
    elev0 = elevs0[wellname][year]
    dtw0 = dtws0[wellname][year] 
    wt0 = wt_offset[0]
    P0 = pressure[0]
    elevs = (wt_offset0 - wt0) +  (elev0 - dtw0) - (pressure-P0) / (g*rho(temp0))
    
    # compare against manual depth to water table measurements -- plot on graph 
    dtw_manual = dtw[icompare]  # icompare gives the index within the notes corresponding to well and year
    iBPmanual = []
    for j in icompare: 
        iBPmanual.append(abs(notetime[j] - BPtime).argmin())    # find index of minimum distance between manual time and BP time
    elevs_manual = (wt_offset0.iloc[iwellmanual].values - wt0) + (elev0 - dtw_manual.values) - (pressure[iBPmanual].values-P0) / (g*rho(temp0.iloc[iwellmanual].values))

    # plot after conversion to elevation
    plt.figure(figsize=(8,3))
    plt.title(wellname+', '+year)
    plt.locator_params(nbins=10, axis='x')
    plt.plot( elevs)
    plt.plot( iwellmanual, elevs_manual, 'o', ms=5)
    
    yesrain = np.where(precip2>0)[0]
    plt.vlines(yesrain, BAR_ELEV, BAR_ELEV+precip2.iloc[yesrain])
    plt.hlines(BAR_ELEV, 0, len(precip2))
    plt.show()

''' WRITE TO  FILE '''
if save_to_excel:
    from openpyxl import load_workbook
    def save_to_excel(df, path, sheet_name): 
        book = load_workbook(path)
        writer = pd.ExcelWriter(path, engine = 'openpyxl')
        writer.book = book
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()
        writer.close()
        
    # lend = min(len(precip2), len(well_time0))
    # df = pd.DataFrame({'Time': well_time0.tolist()[:lend], 'WTE': elevs.tolist()[:lend], 'PRE': precip2[:lend]})
    # path = folderpath + 'processed.xlsx'
    # save_to_excel(df, path, wellname+', '+year)
    
    df = pd.DataFrame({'Time':notetime[icompare], 'Elevs_manual': elevs_manual})
    path = folderpath + 'processed_manual_meas.xlsx'
    save_to_excel(df, path, wellname+', '+year)
   
    



