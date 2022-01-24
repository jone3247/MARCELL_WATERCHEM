#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 14:27:57 2020

@author: xuefeng
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


filepath = '/Users/xuefeng/Desktop/Peatland/Well_data/edi.562.1/MEF_daily_peatland_water_table.xlsx'
sheet_name = 'S2'

bwdata = pd.read_excel(filepath, sheet_name=sheet_name)
date = bwdata['DATE']
wte = bwdata['WTE']

year = 2018
tstart = dt.datetime(year,1,1)
tend = dt.datetime(year,12,31)
istart = np.argmin(np.abs(date - tstart))
iend = np.argmin(np.abs(date - tend))

plt.plot(date[istart:iend], wte[istart:iend])
plt.show()
