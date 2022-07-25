## Marcell Experimental Forest - Well Water Level Data

[Insert abstract summary of the data package here when we have it]

This repository contains the cleaning codes and raw and processed data for data publication to Environmental Data Initative (EDI). This repository is created for the purpose of increasing reproducibilty and transparency within the science community. If you have questions or suggestions on how to improve this cleaning process please don't hesitate to contact me, MW Jones, here on GitHub or at jone3247@umn.edu. 

Reserved Package ID: edi.1126.1

### Contents

**Codes**

codes - Cleaning codes developed by XF and adjusted by MJ. The designated workflow is as follows:  1. Manually identify the index for 'fixing' offset breakpoints 2. Update breakpoint dictionary 3. Automatically fix 4. loop through all wellnames and years (if using the looped code). 

bin - Old cleaning codes. 

**Data Files**

Raw_from_Anne - Level logger data directly from wells at Marcell. Collected by Anne G, research technician at the Marcell Experimental Forest. Includes notes about level logger installation/removal and when downloads were taken. 

consolidated logger.xlsx - Compiled Raw Data. No cleaning.

01_filled_data.xlsx - Cleaned and Filled Data, needs further QAQC. 
