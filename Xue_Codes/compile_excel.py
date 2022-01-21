#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:09:30 2021

@author: xuefeng

Columns: Date/Time, LoggerLevel, LoggerTemp, BP, Precip, Elev0, DTW0
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
save = True
for wellname in ['S2S1', 'S2S2', 'S2S3', 'S6S1', 'S6S2', 'S6S3', 'S6N1', 'S6N2', 'S6N3']:
    for year in ['2019']:
        # year = '2019'
        # wellname = 'KF43W' # KF42W, KF43W, KF45W, S2S(1-3), S6S(1-3), S6N(1-3)
    
        print(wellname, year)

    
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
        # per 1/2 hourly data
        preciptime2 = preciptime[istart:iend][::2]
        precip2 = precipdata[istart:iend].groupby(precipdata[istart:iend].index // 2).sum() # summed to 1/2 hourly
        
        # import BP data 
        if year =='2018':   
            BP = pd.read_excel(BPpath, sheet_name=year, parse_dates={'Date_Time':['Year', 'DoY', 'Hours', 'Minutes']}, 
                                date_parser = lambda x: dt.datetime.strptime(x, '%Y %j %H %M'))
        if year=='2019': BP = pd.read_excel(BPpath, sheet_name=year, parse_date=[['Date_Time']])
        pressure = BP['BP_norm'][:]  # kPa
        BPtime = BP['Date_Time'][:]
        P0 = pressure[0]
        
        ''' find temperature and pressure data closest to each well measurement '''
        atm_arr = np.zeros((len(welltime), 2))
        for iw, wellt in enumerate(welltime): 
            ipressure = np.argmin(abs(BPtime - wellt))
            iprecip = np.argmin(abs(preciptime2 - wellt))
            atm_arr[iw, 0] = pressure.iloc[ipressure]
            atm_arr[iw, 1] = precip2.iloc[iprecip]
        
        ''' find dtw notes closest to each well measurement '''
        df = notetime[imanual].dt.year == int(year)
        icompare = df[df==True].index                                   # find index in notetime corresponding to given year
        iwellmanual = []
        for j in icompare: 
            iwellmanual.append(abs(notetime[j] - welltime).argmin())    # find index of minimum distance between manual time and well time
            
        notes_arr = np.zeros(len(welltime))
        for iw, ic in zip(iwellmanual, icompare): 
            notes_arr[iw] = dtw[ic]
        
        ''' construct a panda dataframe and write to excell ''' 
        
        df_consolidated = pd.DataFrame({
                            'DateTime': welltime.dt.strftime("%Y-%m-%d %H:%M").values, 
                            'LoggerLevel (m)': wt, 
                            'LoggerTemp (C)': temp, 
                            'BP (kPa)': atm_arr[:,0], 
                            'Precip (?)': atm_arr[:,1], 
                            'DTW (m)': notes_arr, 
                           }
                          )
        
        def save_to_excel(df, path, sheet_name): 
            book = load_workbook(path)
            writer = pd.ExcelWriter(path, engine = 'openpyxl')
            writer.book = book
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()
            writer.close()
            
        if save: 
            from openpyxl import load_workbook
            save_to_excel(df_consolidated, path=folderpath + 'welldata_consolidated.xlsx',  sheet_name=wellname+', '+year)


    



