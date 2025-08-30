# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 16:19:36 2025

@author: 杨汉全210
"""

import zipfile
import os
import xarray as xr
from tqdm import tqdm
import time

# ------------------!!输入输出修改--------------------
folder = r"F:\wind_wave\REANALYSIS\2021"      # 存放 zip 的文件夹
output_dir1 = r"F:\wind_wave\REANALYSIS\2021"    # 输出解压结果文件夹
output_dir2 = r"F:\wind_wave\yearly"    # 输出合并结果文件夹
merged_file_name = "wind_2021.nc"
time_dimension_name = 'time'

# ------------------输入输出修改--------------------

def process_zip(zip_path, output_dir):
    # 解压路径
    extract_dir = os.path.splitext(zip_path)[0]
    os.makedirs(extract_dir, exist_ok=True)
    
    # 1. 解压
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    

    # 2. 找 nc 文件
    nc_files = [os.path.join(extract_dir, f) for f in os.listdir(extract_dir) if f.endswith(".nc")]
    if len(nc_files) < 2:
        print(f"⚠ {zip_path} contains less than 2 nc files, skipped.")
        return

    # 3. 合并
    datasets = [xr.open_dataset(nc) for nc in nc_files]
    try:
        merged_ds = xr.merge(datasets)  # 按变量合并
    except Exception:
        merged_ds = xr.concat(datasets, dim="time")  # 按时间拼接

    # 4. 保存到 output_dir
    os.makedirs(output_dir, exist_ok=True)
    merged_name = os.path.splitext(os.path.basename(zip_path))[0] + ".nc" #!! 合并文件名
    output_nc = os.path.join(output_dir, merged_name)
    merged_ds.to_netcdf(output_nc)

    # 5. 关闭并删除临时 nc
    for ds in datasets:
        ds.close()
    for nc in nc_files:
        os.remove(nc)
    os.rmdir(extract_dir)  # 删除解压目录（若为空）


def batch_process(folder, output_dir="merged_output"):
    zip_files = [f for f in os.listdir(folder) if f.endswith(".zip")]
    
    for file in tqdm(zip_files, desc="Processing ZIPs", unit="file"):
        zip_path = os.path.join(folder, file)
        try:
            if os.path.exists(os.path.join(output_dir, os.path.splitext(file)[0] + ".nc")):
                tqdm.write(f"\n⚠ File already exists, skipped: {zip_path}")
            else:
                process_zip(zip_path, output_dir)
        except Exception as e:
            print(f"❌ Failed to process: {zip_path}, Error: {e}")
    print()

def merge_all_nc(folder, output_dir2, merged_file_name):
    if not os.path.exists(output_dir2):
        os.makedirs(output_dir2)
        print(f"Output folder '{output_dir2}' created.")
    else:
        print(f"Output folder '{output_dir2}' already exists.")
    output_nc = os.path.join(output_dir2, merged_file_name)
    # 找到所有 nc 文件
    nc_files = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".nc")])
    
    if not nc_files:
        raise ValueError("❌ No nc files found!")
    
    print(f"Found {len(nc_files)} nc files, start merging...")
    
    # 打开并拼接（自动按 time 维度合并）
    ds = xr.open_mfdataset(nc_files, combine="by_coords",preprocess=lambda x: x.sortby("time"))
    
    # 保存结果
    ds.to_netcdf(output_nc)
    print(f"✅ Merge completed, saved as {output_nc}")
    ds = xr.open_dataset(os.path.join(output_dir2, merged_file_name),
            engine="netcdf4")
    print("-" * 50)  
    print()
    print("merged nc file:", merged_file_name)
    print()
    print("-" * 50)  
    print()
    print("var: ", list(ds.variables),"\n")
    print(ds)
    ds.close()
    print()
        
        

def merge_split_nc(folder, output_dir2, merged_file_name, group_size=10, time_dimension_name='time'):
    """
    Merge NC files in folder.
    If total NC files > group_size, merge every 'group_size' files as one group.
    After each merge, print variable list and time range.
    """
    if not os.path.exists(output_dir2):
        os.makedirs(output_dir2)
        print(f"Output folder '{output_dir2}' created.")
    else:
        print(f"Output folder '{output_dir2}' already exists.")
    output_nc = os.path.join(output_dir2, merged_file_name)
    
    time_dim = time_dimension_name
    
    # 找到所有 nc 文件
    nc_files = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".nc")])
    
    if not nc_files:
        raise ValueError("❌ No nc files found!")

    print(f"Found {len(nc_files)} nc files, start merging in groups of {group_size}...")

    # 分组合并
    for i in range(0, len(nc_files), group_size):
        group_files = nc_files[i:i+group_size]
        group_index = i // group_size + 1
        output_nc = os.path.join(output_dir2, f"merged_group{group_index}.nc")
        
        print(f"\n⏳ Merging group {group_index} ({len(group_files)} files)...")
        ds = xr.open_mfdataset(group_files, combine="by_coords")
        
        # 保存合并结果
        ds.to_netcdf(output_nc)
        print(f"✅ Group {group_index} merged, saved as {output_nc}")
        
        # 打印变量列表和时间范围
        print("Variables:", list(ds.variables))
        print(ds)
        
        ds.close()
        
        

if __name__ == "__main__":
    start_time = time.time()
    print('\nProcess begin!\n')
    print("-" * 50)  
    print()
    #!! 开启解压文件功能
    # batch_process(folder, output_dir1) 
    print()
    print("-" * 50)  
    print() 
    if os.path.exists(os.path.join(folder, merged_file_name)):
        print(f"File {os.path.join(folder, merged_file_name)} already exists.\n")

    else:
    # #!! 开启合并时序文件功能(不分组)
        merge_all_nc(folder, output_dir2, merged_file_name)
    # #!! 开启合并时序文件功能(分组)
        # merge_split_nc(folder, output_dir2, merged_file_name, group_size=40,
        #                time_dimension_name=time_dimension_name)
    end_time = time.time()
    elapsed = end_time - start_time
    
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = elapsed % 60
    print("-" * 50)  
    print('\nprocess finished!\n') 
    print(f"total time: {hours}h {minutes}m {seconds:.2f}s")
    
        




