#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 10:52:03 2021

@author: xuefeng
"""
# Temperature breakpoints 
temppt_dict = {'KF42W':{'2018': {'istart':0, 'ibefore':[1102,1154,1494,1733,2020,3174,4422], 'iafter':[1111,1176,1516,1748,2037,3176,4425], 'fill_opt':[0,0,0,0,0,0,1]},
                        },
               'KF43W':{'2018': {'istart':0, 'ibefore':[1062, 1154, 1494, 1733,2020,4422], 'iafter':[1072,1162,1525,1743,2028,4425], 'fill_opt':[0,0,0,0,0,1]},
                        },
               'KF45W':{'2018': {'istart':0, 'ibefore':[1013,1061,1153,1493,1732,2019,4083,4421], 'iafter':[1018,1077,1162,1500,1769,2026,4086,4425],'fill_opt':[0,0,0,0,0,0,0,1]},
                        },
                }

# Water table elevation breakpoints
# fill_options: 0 - default; linearly interpolate between before and after; 1: patch before and after by calculating offset 
wtept_dict = {'KF42W':{'2018': {'istart':0, 'ibefore':[1102,1154,1494,1733,2020,3174,4422], 'iafter':[1111,1156,1496,1735,2022,3176,4425], 'fill_opt':[1,0,0,0,0,0,1]},
                         '2019': {'istart':0, 'ibefore':[0, 7349], 'iafter':[1, 7352], 'fill_opt':[1,1]},
                         '2020': {'istart':1, 'ibefore':[0], 'iafter':[1], 'fill_opt':[1]}
                        },
                'KF43W':{'2018': {'istart':0, 'ibefore':[1062, 1153, 1494, 1733,4422], 'iafter':[1064, 1155, 1496, 1735,4425], 'fill_opt':[1,1,1,1,1]},
                         '2019': {'istart':0, 'ibefore':[0,7349], 'iafter':[1,7352], 'fill_opt':[1,1]},
                         '2020': {'istart':1, 'ibefore':[9412], 'iafter':[9415], 'fill_opt':[1,1]}
                        },
                'KF45W':{'2018': {'istart':0, 'ibefore':[1013,1061,1153,1493,1732,2019,4421], 'iafter':[1015,1063, 1157,1495,1734,2021,4425],'fill_opt':[1,0,0,0,0,0,1]},
                         '2019': {'istart':0, 'ibefore':[0,9078], 'iafter':[1, 9081], 'fill_opt':[1,1]},
                         '2020': {'istart':1, 'ibefore':[9411], 'iafter':[9414], 'fill_opt':[1]}
                         },
                'S2S1':{'2019': {'istart':38, 'ibefore':[38, 2060], 'iafter':[41, 2063], 'fill_opt':[1,1]}, 
                        '2020': {'istart':0, 'ibefore':[0], 'iafter':[2], 'fill_opt':[1]}
                        },
                'S2S2':{'2019': {'istart':38, 'ibefore':[38, 2060], 'iafter':[41, 2063], 'fill_opt':[1,1]},
                        '2020': {'istart':0, 'ibefore':[0, 9313], 'iafter':[2, 9319], 'fill_opt':[1,1]}
                        },
                'S2S3':{'2019': {'istart':38, 'ibefore':[38, 1816], 'iafter':[42, 1821], 'fill_opt':[1,1]},
                        '2020': {'istart':0, 'ibefore':[0, 9313], 'iafter':[2, 9319], 'fill_opt':[1,1]}
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



            