#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 10:52:03 2021

@author: xuefeng
"""
# Temperature breakpoints 
temppt_dict = {'KF42W':{'2018': {'istart':0, 'ibefore':[1102,1154,1494,1733,2020,3174,4422], 'iafter':[1111,1176,1516,1748,2037,3176,4425], 'fill_opt':[0,0,0,0,0,0,1]},
                        '2019': {'istart':5, 'ibefore':[1680, 3990, 5534, 7349], 'iafter':[1683, 3993, 5537, 7782], 'fill_opt':[0, 0, 0, 1]}, 
                        '2020': {'istart':5, 'ibefore':[], 'iafter':[], 'fill_opt':[]}
                        },
               'KF43W':{'2018': {'istart':0, 'ibefore':[1062,1154,1494,1733,2020,4422], 'iafter':[1072,1162,1525,1743,2028,4425], 'fill_opt':[0,0,0,0,0,1]},
                        '2019': {'istart':5, 'ibefore':[1680, 3990, 5331, 5379, 7349], 'iafter':[1683, 3993, 5334, 5382, 7782], 'fill_opt':[0, 0, 0, 0, 1]}, 
                        '2020': {'istart':5, 'ibefore':[1345, 5379, 9412], 'iafter':[1348, 5382, 9690], 'fill_opt':[0, 0, 1]}
                        },
               'KF45W':{'2018': {'istart':0, 'ibefore':[1013,1061,1153,1493,1732,2019,4083,4421], 'iafter':[1018,1077,1162,1500,1769,2026,4086,4425],'fill_opt':[0,0,0,0,0,0,0,1]},
                        '2019': {'istart':5, 'ibefore':[965, 1728, 3407, 5717, 7081, 9078], 'iafter': [968, 1731, 3410, 5720, 7084, 9510], 'fill_opt':[0,0,0,0,0,1]},
                        '2020': {'istart':0, 'ibefore':[1343, 5377, 9410], 'iafter':[1347, 5381, 9689], 'fill_opt':[0, 0, 1]}
                        },
               'S2S1':{'2019': {'istart':38, 'ibefore':[2060], 'iafter':[2494], 'fill_opt':[1]}, #Cannot remove the first blip because of the manual checkpoint at index 38
                       '2020': {'istart':0, 'ibefore':[1343], 'iafter':[1348], 'fill_opt':[0]}
                        },
               'S2S2':{'2019': {'istart':38, 'ibefore':[2060], 'iafter':[2075], 'fill_opt':[1]},
                       '2020': {'istart':0, 'ibefore':[1344, 5378, 5868, 9311], 'iafter':[1348, 5382, 5872, 9356], 'fill_opt':[0, 0, 0, 1]} #Cannot remove the first blip because of the manual checkpoints
                        },
               'S2S3':{'2019': {'istart':39, 'ibefore':[1815], 'iafter':[2494], 'fill_opt':[1]},
                       '2020': {'istart':0, 'ibefore':[1344, 5378, 9312], 'iafter':[1348, 5382, 9356], 'fill_opt':[0, 0,1]}  #Cannot remove the first blip because of the manual checkpoints
                        },
                }

# Water table elevation breakpoints
# fill_options: 0 - default; linearly interpolate between before and after; 1: patch before and after by calculating offset 
wtept_dict = {'KF42W':{'2018': {'istart':0, 'ibefore':[1102,1154,1494,1733,2020,3174,4422], 'iafter':[1111,1156,1496,1735,2022,3176,4425], 'fill_opt':[1,0,0,0,0,0,1]},
                         '2019': {'istart':5, 'ibefore':[2200, 4677, 5756, 7349], 'iafter':[2203, 4680, 5759, 7355], 'fill_opt':[0, 0, 0,1]},
                         '2020': {'istart':5, 'ibefore':[378], 'iafter':[381], 'fill_opt':[0]}
                        },
                'KF43W':{'2018': {'istart':0, 'ibefore':[1062, 1153, 1494, 1733,4422], 'iafter':[1064, 1155, 1496, 1735,4425], 'fill_opt':[1,1,1,1,1]},
                         '2019': {'istart':5, 'ibefore':[0, 2201, 4675, 5756, 7347], 'iafter':[3, 2204, 4678, 5759, 7350], 'fill_opt':[0, 0, 0, 0,1]},
                         '2020': {'istart':5, 'ibefore':[1813, 4841, 6042, 7119, 7233, 8250, 8591, 9358], 'iafter':[1816, 4844, 6045, 7122, 7236, 8253, 8594, 9361], 'fill_opt':[0, 0, 0, 0, 0, 0, 0,1]}
                        },
                'KF45W':{'2018': {'istart':0, 'ibefore':[1013,1061,1153,1493,1732,2019,4421], 'iafter':[1015,1063, 1157,1495,1734,2021,4425],'fill_opt':[1,0,0,0,0,0,1]},
                         '2019': {'istart':0, 'ibefore':[0, 283, 3929, 6405, 7484, 9077], 'iafter':[1, 286, 3932, 6408, 7487, 9080], 'fill_opt':[0, 0, 0, 0, 0, 1]}, 
                         '2020': {'istart':0, 'ibefore':[1812, 4839, 6041, 7233, 7240, 8248, 8590, 9356], 'iafter':[1815, 4842, 6043, 7236, 7243, 8252, 8593, 9359], 'fill_opt':[0, 0, 0, 0, 0, 0, 0, 1]}
                         },
                'S2S1':{'2019': {'istart':38, 'ibefore':[467, 1431, 2060], 'iafter':[470, 1434, 2070], 'fill_opt':[0, 0, 1]}, #Cannot remove the first blip because of the manual checkpoint at index 38
                        '2020': {'istart':0, 'ibefore':[1146, 1812], 'iafter':[1149, 1815], 'fill_opt':[0, 0]}
                        },
                'S2S2':{'2019': {'istart':38, 'ibefore':[464, 1431, 2058], 'iafter':[468, 1435, 2062], 'fill_opt':[0, 0, 1]},
                        '2020': {'istart':0, 'ibefore':[1145, 1811, 4839, 4937, 6041, 8232, 8247, 8590], 'iafter':[1149, 1815, 4843, 4941, 6045, 8236, 8251, 8595], 'fill_opt':[0, 0, 0, 0, 0, 0, 0, 0]} #Cannot remove the first blip because of the manual checkpoints
                        },
                'S2S3':{'2019': {'istart':39, 'ibefore':[466, 1431, 1815], 'iafter':[470, 1435, 1820], 'fill_opt':[0, 0, 1]},
                        '2020': {'istart':0, 'ibefore':[1812, 4936, 6042, 8248, 8590, 9312], 'iafter':[1816, 4940, 6046, 8252, 8595, 9316, 9356], 'fill_opt':[0, 0, 0, 0, 0, 0, 1]}  #Cannot remove the first blip because of the manual checkpoints
                        },
                
                'S6N1':{'2019': {'istart':0, 'ibefore':[13], 'iafter':[14], 'fill_opt':[1]}, 
                        '2020': {'istart':0, 'ibefore':[5732], 'iafter':[5734], 'fill_opt':[1]}, # small patch outside of calibration points
                        },
                'S6N2':{'2019': {'istart':0, 'ibefore':[13], 'iafter':[14], 'fill_opt':[1]}, 
                        '2020': {'istart':0, 'ibefore':[15384], 'iafter':[15385], 'fill_opt':[1]},
                        },
                'S6N3':{'2019': {'istart':0, 'ibefore':[13], 'iafter':[14], 'fill_opt':[1]}, 
                        '2020': {'istart':0, 'ibefore':[15384], 'iafter':[15385], 'fill_opt':[1]},
                        },
                'S6S1':{'2019': {'istart':2, 'ibefore':[2, 2023], 'iafter':[3, 2031], 'fill_opt':[1,1]},
                        '2020': {'istart':0, 'ibefore':[0, 5375, 9308], 'iafter':[1, 5377, 9317], 'fill_opt':[1,1,1]},
                        },
                'S6S2':{'2019': {'istart':2, 'ibefore':[2, 2023], 'iafter':[5, 2031], 'fill_opt':[1,1]},
                        '2020': {'istart':0, 'ibefore':[0, 5375, 9308], 'iafter':[1, 5377, 9317], 'fill_opt':[1,1,1]},
                        },
                'S6S3':{'2019': {'istart':2, 'ibefore':[2, 2023], 'iafter':[3, 2029], 'fill_opt':[1,1]},
                        '2020': {'istart':0, 'ibefore':[0, 9308], 'iafter':[1, 9317], 'fill_opt':[1,1,1]},
                        }
                }



            