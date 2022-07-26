#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 10:52:03 2021

@author: xuefeng
"""
# Temperature breakpoints 
temppt_dict = {'KF42W':{'2018': {'istart':0, 'ibefore':[1102,1154,1494,1733,2020,3174,4422], 'iafter':[1111,1176,1516,1748,2037,3176,4425], 'fill_opt':[0,0,0,0,0,0,1]},
                         '2019': {'istart':2, 'ibefore':[1678, 3988, 5541, 7349], 'iafter':[1682, 3992, 5541, 7782], 'fill_opt':[0, 0, 0,1]},
                         '2020': {'istart':1, 'ibefore':[376], 'iafter':[380], 'fill_opt':[0]}
                        },
               'KF43W':{'2018': {'istart':0, 'ibefore':[1062, 1154, 1494, 1733,2020,4422], 'iafter':[1072,1162,1525,1743,2028,4425], 'fill_opt':[0,0,0,0,0,1]},
                         '2019': {'istart':2, 'ibefore':[1678, 3988, 5329, 5377, 7349], 'iafter':[1682, 3992, 5333, 5381, 7776], 'fill_opt':[0, 0, 0, 0, 1]},
                         '2020': {'istart':1, 'ibefore':[1343, 5377, 9410], 'iafter':[1347, 5381, 9665], 'fill_opt':[0, 0 ,1]}
                        },
               'KF45W':{'2018': {'istart':0, 'ibefore':[1013,1061,1153,1493,1732,2019,4083,4421], 'iafter':[1018,1077,1162,1500,1769,2026,4086,4425],'fill_opt':[0,0,0,0,0,0,0,1]},
                        '2019': {'istart':2, 'ibefore':[964, 1727, 3406, 5716, 7080, 9078], 'iafter':[968, 1731, 3410, 5720, 7084, 9510],'fill_opt':[0, 0, 0, 0, 0, 1]},
                        '2020': {'istart':0, 'ibefore':[1342, 5376, 9410], 'iafter':[1346, 5380, 9689],'fill_opt':[0, 0, 1]},
                        },
               'S2S1':{'2019': {'istart':38, 'ibefore':[2060], 'iafter':[2070], 'fill_opt':[1]}, 
                        '2020': {'istart':0, 'ibefore':[0, 1343], 'iafter':[1, 1347], 'fill_opt':[0, 0]}
                        },
               'S2S2':{'2019': {'istart':38, 'ibefore':[2060], 'iafter':[2075], 'fill_opt':[1]},
                        '2020': {'istart':0, 'ibefore':[1344, 5378, 5868, 9311], 'iafter':[1348, 5382, 5872, 9356], 'fill_opt':[0, 0, 0, 1]}
                        },
               'S2S3':{'2019': {'istart':39, 'ibefore':[1815], 'iafter':[2494], 'fill_opt':[1]},
                        '2020': {'istart':0, 'ibefore':[1344, 5378, 9312], 'iafter':[1348, 5382, 9356], 'fill_opt':[0, 0, 1]}
                        },
                
               'S6N1':{'2019': {'istart':2, 'ibefore':[3], 'iafter':[14], 'fill_opt':[1]}, 
                        '2020': {'istart':0, 'ibefore':[6075, 7419], 'iafter':[6079, 7424], 'fill_opt':[0, 0]} # small patch outside of calibration points
                        },
               'S6N2':{'2019': {'istart':14, 'ibefore':[ ], 'iafter':[ ], 'fill_opt':[ ]}, 
                        '2020': {'istart':0, 'ibefore':[6075, 7419, 11450, 15384], 'iafter':[6079, 7423, 11454, 15430], 'fill_opt':[0,0, 0, 1]}
                        },
               'S6N3':{'2019': {'istart':15, 'ibefore':[ ], 'iafter':[ ], 'fill_opt':[ ]}, 
                        '2020': {'istart':0, 'ibefore':[6074, 7419, 11448, 11983, 12029, 12076, 15384], 'iafter':[6078, 7423, 11452, 11987, 12033, 12080, 15431], 'fill_opt':[0, 0, 0, 0, 0, 0, 1]}
                        },
               'S6S1':{'2019': {'istart':3, 'ibefore':[2022], 'iafter':[2042], 'fill_opt':[1]},
                        '2020': {'istart':3, 'ibefore':[1343, 5374, 9308], 'iafter':[1347, 5378, 9354], 'fill_opt':[0, 0,1]}
                        },
               'S6S2':{'2019': {'istart':3, 'ibefore':[2022], 'iafter':[2041], 'fill_opt':[1]},
                        '2020': {'istart':3, 'ibefore':[1343, 3213, 3287, 3649, 5374, 6941, 7325, 7349, 7368, 7388, 7408, 7476, 8804, 9308], 'iafter':[1347, 3217, 3291, 3653, 5378, 6945, 7329, 7353, 7372, 7392, 7412, 7480, 8808, 9353], 'fill_opt':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}
                        },
               'S6S3':{'2019': {'istart':2, 'ibefore':[2, 2023], 'iafter':[3, 2029], 'fill_opt':[0, 1]},
                        '2020': {'istart':0, 'ibefore':[1343, 5374, 5709, 9308], 'iafter':[1347, 5378, 5713, 9333], 'fill_opt':[0, 0, 0, 1]}
                        }
               }

# Water table elevation breakpoints
# fill_options: 0 - default; linearly interpolate between before and after; 1: patch before and after by calculating offset 
wtept_dict = {'KF42W':{'2018': {'istart':0, 'ibefore':[1102,1154,1494,1733,2020,3174,4422], 'iafter':[1111,1156,1496,1735,2022,3176,4425], 'fill_opt':[1,0,0,0,0,0,1]},
                         '2019': {'istart':2, 'ibefore':[2197, 4674, 5753, 7348], 'iafter':[2202, 4679, 5758, 7352], 'fill_opt':[0, 0, 0, 1]},
                         '2020': {'istart':0, 'ibefore':[0], 'iafter':[3], 'fill_opt':[1]}
                        },
              'KF43W':{'2018': {'istart':0, 'ibefore':[1062, 1153, 1494, 1733,4422], 'iafter':[1064, 1155, 1496, 1735,4425], 'fill_opt':[1,1,1,1,1]},
                         '2019': {'istart':2, 'ibefore':[2299, 4673, 5754, 7345], 'iafter':[2203, 4677, 5758,7352], 'fill_opt':[0, 0, 0, 1]},
                         '2020': {'istart':2, 'ibefore':[1811, 4839, 6040, 7117, 7231, 8248, 8589, 9356, 9410], 'iafter':[1815, 4833, 6044, 7121, 7235, 8252, 8593, 9360, 9414], 'fill_opt':[0, 0, 0, 0, 0, 0, 0,0, 1]}
                        },
              'KF45W':{'2018': {'istart':0, 'ibefore':[1013,1061,1153,1493,1732,2019,4421], 'iafter':[1015,1063, 1157,1495,1734,2021,4425],'fill_opt':[1,0,0,0,0,0,1]},
                         '2019': {'istart':2, 'ibefore':[282, 3928, 6404, 7483, 9076], 'iafter':[286, 3932, 6408, 7487, 9081], 'fill_opt':[0, 0, 0, 0, 1]},
                         '2020': {'istart':0, 'ibefore':[1810, 4837, 6039, 7231, 7238, 8246, 8588, 9354, 9409], 'iafter':[1814, 4841, 6033, 7235, 7242, 8250, 8592, 9358, 9509], 'fill_opt':[0, 0, 0, 0, 0, 0, 0, 0, 1]}
                         },
              'S2S1':{'2019': {'istart':0, 'ibefore':[35, 2060], 'iafter':[39, 2063], 'fill_opt':[1, 1]}, 
                        '2020': {'istart':0, 'ibefore':[0, 1144, 1810], 'iafter':[2, 1148, 1818], 'fill_opt':[1, 0, 0]}
                        },
              'S2S2':{'2019': {'istart':0, 'ibefore':[37, 464, 1431, 2058], 'iafter':[39, 468, 1435, 2062], 'fill_opt':[1, 0, 0, 1]},
                        '2020': {'istart':0, 'ibefore':[0, 1145, 1811, 4839, 4937, 6041, 8232, 8247, 8590, 9311], 'iafter':[2, 1149, 1815, 4843, 4941, 6045, 8236, 8251, 8595, 9315], 'fill_opt':[1, 0, 0, 0, 0, 0, 0, 0, 0, 1]} #Cannot remove the first blip because of the manual checkpoints
                        },
              'S2S3':{'2019': {'istart':39, 'ibefore':[466, 1431, 1815], 'iafter':[470, 1435, 1820], 'fill_opt':[0, 0, 1]},
                        '2020': {'istart':0, 'ibefore':[0, 1812, 4936, 6042, 8248, 8590, 9311], 'iafter':[2, 1816, 4940, 6046, 8252, 8595, 9316, 9315], 'fill_opt':[1, 0, 0, 0, 0, 0, 0, 1]}
                        },
              'S6N1':{'2019': {'istart':0, 'ibefore':[13], 'iafter':[14], 'fill_opt':[1]}, 
                        '2020': {'istart':0, 'ibefore':[5732], 'iafter':[5734], 'fill_opt':[0]}, # small patch outside of calibration points
                        },
              'S6N2':{'2019': {'istart':0, 'ibefore':[13], 'iafter':[14], 'fill_opt':[1]}, 
                        '2020': {'istart':0, 'ibefore':[15384], 'iafter':[15385], 'fill_opt':[1]}
                        },
              'S6N3':{'2019': {'istart':0, 'ibefore':[13], 'iafter':[14], 'fill_opt':[1]}, 
                        '2020': {'istart':0, 'ibefore':[15384], 'iafter':[15385], 'fill_opt':[1]}
                        },
              'S6S1':{'2019': {'istart':0, 'ibefore':[2, 2023], 'iafter':[3, 2031], 'fill_opt':[1,1]},
                        '2020': {'istart':0, 'ibefore':[0, 5375, 9308], 'iafter':[1, 5377, 9317], 'fill_opt':[0,1,1]}
                        },
              'S6S2':{'2019': {'istart':0, 'ibefore':[0, 431, 1397, 2023], 'iafter':[4, 435, 1401, 2029], 'fill_opt':[1, 0, 0, 1]},
                        '2020': {'istart':0, 'ibefore':[0, 5375, 9308], 'iafter':[1, 5377, 9317], 'fill_opt':[0,1,1]}
                        },
              'S6S3':{'2019': {'istart':0, 'ibefore':[0, 2023], 'iafter':[3, 2029], 'fill_opt':[1, 1]},
                        '2020': {'istart':0, 'ibefore':[0, 1809, 4935, 6039, 8246, 8588, 9308], 'iafter':[1, 1814, 4939, 6043, 8250, 8592, 9317], 'fill_opt':[0, 0, 0, 0, 0, 0, 1]}
                        }
                }



            