#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 14:28:42 2020

@author: xuefeng
"""
import xmltodict
import csv


folderpath = "/Users/xuefeng/Desktop/Peatland/Well_data/Organized/Raw from Anne/S2/"
filename = 'KF42W_2018.08.28'
filepath = folderpath + filename + '.xle'


def xml_to_csv(filepath, targetfolderpath):
    with open(filepath) as fd:
        doc = xmltodict.parse(fd.read())
        
    content = doc['Body_xle']
    keys = list(content.keys()) 
     # ['File_info',
     # 'Instrument_info',
     # 'Instrument_info_data_header',
     # 'Ch1_data_header',
     # 'Ch2_data_header',
     # 'Data']
    
    with open(targetfolderpath + filename + '.csv', 'w') as f:
        writer = csv.writer(f)
        for k in keys[:(len(keys)-1)]: 
            for item in list(content[k].items()): 
                writer.writerow(item)
                
        writer.writerow(['LogID', 'Date', 'Time', 'ms', 'LEVEL', 'TEMPERATURE'])
        for item in list(content['Data'].items())[0][1]: 
            writer.writerow(item.values())


from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir(folderpath) if isfile(join(folderpath, f))]
xlmfilenames = [f[:-4] for f in onlyfiles if f[-3:]=='xle']

targetfolderpath = "/Users/xuefeng/Desktop/Peatland/Well_data/Organized/Processed/S2/"
for filename in xlmfilenames:
    xml_to_csv(folderpath+filename+'.xle', targetfolderpath)
    