# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 15:23:45 2025

@author: 杨汉全210
"""

import calc_wind_energy as calc_wind_energy
import os
import glob
import time
from tqdm import tqdm
import xarray as xr


#!!--------------------------------------------
inputfolder = r"F:\wind_wave\yearly"
outputfolder = r"F:\wind_power\yearly"
#----------------------------------------------


# %%
# 确保输出文件夹存在
os.makedirs(outputfolder, exist_ok=True)

start_time = time.time()
print('\nProcess begin!\n')
print("-" * 50)  
print()

inputfile = glob.glob(os.path.join(inputfolder, "wind_*.nc"))
#!!--------------TEST ONLY!!!------------------------
# N = 6
# inputfile = inputfile[:N] 
#----------------------------------------------

names = [os.path.splitext(os.path.basename(f))[0] for f in inputfile]
outputfile = [os.path.join(outputfolder, name + "_power.nc") for name in names]
# %%
for infile, outfile in tqdm(zip(inputfile, outputfile), 
                            total=len(inputfile), 
                            desc="Processing files", 
                            unit="file"):
    if os.path.exists(outfile):
        tqdm.write(f"\n--> Skipping {os.path.basename(outfile)} (already exists)")
        continue
    tqdm.write(f"\n--> Processing {os.path.basename(infile)}")
    calc_wind_energy.calc_wind_energy(infile, outfile)

# %%

end_time = time.time()
elapsed = end_time - start_time

hours = int(elapsed // 3600)
minutes = int((elapsed % 3600) // 60)
seconds = elapsed % 60

print()

if inputfile:
    last_file = inputfile[-1]
    print("\nLast input file information:")
    print(f"File: {last_file}")
    ds_example = xr.open_dataset(last_file)
    print(ds_example.time)
    print(ds_example)
    ds_example.close()

if outputfile:
    last_file = outputfile[-1]
    print("\nLast output file information:")
    print(f"File: {last_file}")
    ds_example = xr.open_dataset(last_file)
    print(ds_example.time)
    print(ds_example)
    ds_example.close()


print("-" * 50)  
print('\nProcess finished!\n') 
print(f"Total time: {hours}h {minutes}m {seconds:.2f}s")
