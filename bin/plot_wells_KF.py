#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 14:21:45 2020

@author: xuefeng
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

folderpath = '/Users/xuefeng/Desktop/Peatland/Well_data/Organized/'
filepath = folderpath + 'processed.xlsx'

year = '2018'
RAIN_LEVEL = 421.5
manual = False
dates = {'2018': {'tstart': dt.datetime(2018,8,7,19), 'tend': dt.datetime(2018,10,12,11,30)}, 
         '2019': {'tstart': dt.datetime(2019,6,6,13), 'tend': dt.datetime(2019,11,13,13)}, 
        }

tstart = dates[year]['tstart']
tend = dates[year]['tend']

''' DATA IMPORT for Bogwell data ''' 
bwdata = pd.read_excel(filepath, sheet_name='S2BW'+ ', ' + year)
bogwte = bwdata['WTE']
bogtime = bwdata['DATE']
istart_bog = np.argmin(np.abs(bogtime - tstart))
iend_bog = np.argmin(np.abs(bogtime - tend))

''' plotting setup '''
plt.figure(figsize=(12,4.5))
plt.plot(bogtime[istart_bog:iend_bog], bogwte[istart_bog:iend_bog], 'o', ms=1, label='bogwell (daily)')

''' DATA IMPORT for manual measurements '''
if manual: 
    sheet_name = 'KF45W, ' + year
    notedata = pd.read_excel(folderpath + 'processed_manual_meas.xlsx', sheet_name=sheet_name)
    notetime = notedata['Time']
    elevs_manual = notedata['Elevs_manual']
    
''' DATA IMPORT for KF gradient'''
gradient = {}
for wn in ['KF42W', 'KF43W', 'KF45W']: 
    # import well data
    sheet_name = wn + ', ' + year
    welldata = pd.read_excel(filepath, sheet_name=sheet_name)
    welltime = welldata['Time']
    wte = welldata['WTE']
    pre = welldata['PRE']
    
    istart = np.argmin(np.abs(welltime - tstart))
    iend = np.argmin(np.abs(welltime - tend))
    
    gradient[wn] = {}
    gradient[wn]['time'] = np.array(welltime[istart:iend])
    gradient[wn]['wte'] = np.array(wte[istart:iend])
    gradient[wn]['pre'] = np.array(pre[istart:iend])
    
    plt.plot(welltime, wte, lw=0.8, label=wn)
    plt.plot(welltime, pre*0.2 + RAIN_LEVEL, color='gray')

if manual:
    plt.plot(notetime, elevs_manual, 'o', ms=5, color='k', mew=0.3, mec='k', label='manual KF45W')
plt.legend() 
plt.tight_layout() 
plt.show()

