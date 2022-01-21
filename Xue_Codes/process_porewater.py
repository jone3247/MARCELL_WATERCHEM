#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 12:31:50 2021

@author: xuefeng
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

''' FOLDER DIRECTORIES'''

bogwaterpath = '/Users/xuefeng/Desktop/Peatland/Well_data/edi.712.2/S2bog_porewater_weekly.csv'
laggwaterpath = '/Users/xuefeng/Desktop/Peatland/Well_data/edi.712.2/S2lagg_porewater_weekly.csv'
precippath = '/Users/xuefeng/Desktop/Peatland/Well_data/edi.563.1/MEF_precipitation_daily.csv'

precip = pd.read_csv(precippath)
bog = pd.read_csv(bogwaterpath)
lagg = pd.read_csv(laggwaterpath)

bog['Date'] = pd.to_datetime(bog['DateTime']).dt.date
lagg['Date'] = pd.to_datetime(lagg['DateTime']).dt.date
precip['Date'] = pd.to_datetime(precip['DATE']).dt.date

bog['Year'] = pd.to_datetime(bog['DateTime']).dt.year
lagg['Year'] = pd.to_datetime(lagg['DateTime']).dt.year
precip['Year'] = pd.to_datetime(precip['DATE']).dt.year

bog['doy'] = pd.to_datetime(bog['DateTime']).dt.dayofyear
lagg['doy'] = pd.to_datetime(lagg['DateTime']).dt.dayofyear

# Index(['LAB_ID', 'PIEZOMETER', 'DateTime', 'PH', 'SPCOND', 'CL', 'SO4', 'CA',
       # 'K', 'MG', 'Na', 'AL', 'FE', 'MN', 'SI', 'SR', 'NH4', 'NO3', 'SRP',
       # 'TN', 'TP', 'TOC', 'O18', 'D', 'FEII', 'FEIII'],

chem = 'SO4'; title = chem
laggwell = 'KF5'       
bogwell = 'KF45' # 'KF5A'  

laggwell_df = lagg[lagg.PIEZOMETER==laggwell]
bogwell_df = bog[bog.PIEZOMETER==bogwell]

laggdate = laggwell_df['Date']
laggchems = laggwell_df[chem]
laggchems = laggchems.mask(laggchems==-9999, np.nan)

bogdate = bogwell_df['Date']
bogchems = bogwell_df[chem]
bogchems = bogchems.mask(bogchems==-9999, np.nan)

startyear = 2011
precipdate = precip[precip.Year>=startyear]['Date']
precipvals = precip[precip.Year>=startyear]['South_PCP']

#%%
ms=3

f, (a0, a1) = plt.subplots(1, 2, figsize=(11,3), gridspec_kw={'width_ratios': [3.5, 1]})

a0.set_title(title)
# a0.plot(precipdate, 0.1*precipvals.rolling(window=14).sum(), color='lightgrey')
a0.plot(precipdate, 0.1*precipvals, color='lightgrey')
a0.plot(laggdate, laggchems,'o', ms=ms, label='lagg')
a0.plot(bogdate, bogchems, 'o', ms=ms, label='bog')
# a0.plot(bogdate, laggchems - bogchems, 'o', ms=ms, label='difference (lagg-bog)')
a0.set_xlabel('Date')
a0.legend()

a1.set_title('Seasonal average')
a1.plot(laggwell_df['doy'], laggchems,'o', ms=ms)
a1.plot(bogwell_df['doy'], bogchems, 'o', ms=ms)
a1.set_xlabel('DOY')
plt.tight_layout()
plt.show()


# #%% SUPERIMPOSE YEARS TO SEE IF THEY SHOW SIMILAR DYNAMIC as hydraulic gradients 

# bog_pivot = pd.pivot_table(bogwell_df, index=['Year', 'doy'])
# lagg_pivot = pd.pivot_table(laggwell_df, index=['Year', 'doy'])
