# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 10:35:14 2025

@author: 杨汉全210
"""

import xarray as xr
import geopandas as gpd
import rioxarray
from shapely.geometry import mapping
import os
import numpy as np

#!!----------------------input/output---------------
nc_folder=r"F:\wind_power\yearly_mean"
shp_file=r"E:/AAAAA\HQD/land_mask/FAB_final_land_mask.shp"
output_folder=r"F:\wind_power\yearly_mean_only_masked"
#---------------------------------------------------


def mask_nc_with_shp(nc_folder, shp_file, output_folder, invert=True):
    """
    使用shp文件掩膜NetCDF文件 (批量处理文件夹)
    
    参数:
        nc_folder (str): 输入nc文件夹路径
        shp_file (str): 掩膜用的shapefile路径
        output_folder (str): 输出nc文件夹路径
        invert (bool): True表示保留shp外部 (即陆地变NaN, 海洋保留);
                       False表示保留shp内部 (即陆地保留, 海洋NaN)
    """
    # 检查并创建输出目录
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📂 Le dossier de sortie n'existait pas, il a été créé : {output_folder}")
    else:
        print(f"📂 Le dossier de sortie existe déjà : {output_folder}")
        
    # 读取shapefile
    gdf = gpd.read_file(shp_file)
    
    # 确保输出目录存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 遍历文件夹中的 nc 文件
    for fname in os.listdir(nc_folder):
        if fname.endswith(".nc"):
            in_path = os.path.join(nc_folder, fname)
            out_path = os.path.join(output_folder, fname.replace(".nc", "_masked.nc"))
            
            print(f"正在处理: {fname}")
            
            # 打开 nc
            ds = xr.open_dataset(in_path)
            
            # 设置 CRS (若无)
            if not ds.rio.crs:
                ds = ds.rio.write_crs("EPSG:4326")
            
            # shapefile 投影一致
            if gdf.crs != ds.rio.crs:
                gdf = gdf.to_crs(ds.rio.crs)
            
            # 掩膜
            ds_masked = ds.rio.clip(
                gdf.geometry.apply(mapping),
                gdf.crs,
                invert=invert
            )
            
            for var in ds_masked.data_vars:
                dims = ds_masked[var].dims
                # 只处理二维或三维变量（含 lat/lon）
                if "lat" in dims and "lon" in dims:
                    arr = ds_masked[var].values
                    # 四条边置为 NaN
                    if arr.ndim == 2:
                        arr[0, :] = np.nan       # 上边
                        arr[-1, :] = np.nan      # 下边
                        arr[:, 0] = np.nan       # 左边
                        arr[:, -1] = np.nan      # 右边
                    elif arr.ndim == 3:  # time x lat x lon
                        arr[:, 0, :] = np.nan
                        arr[:, -1, :] = np.nan
                        arr[:, :, 0] = np.nan
                        arr[:, :, -1] = np.nan
                    elif arr.ndim == 4:  # time x depth x lat x lon
                        arr[:, :, 0, :] = np.nan
                        arr[:, :, -1, :] = np.nan
                        arr[:, :, :, 0] = np.nan
                        arr[:, :, :, -1] = np.nan
                    ds_masked[var].values = arr
        
            # 保存
            if 'spatial_ref' in ds_masked.data_vars:
                ds_masked = ds_masked.drop_vars('spatial_ref')
            ds_masked.to_netcdf(out_path)
            print(f"已保存到: {out_path}\n")
            print(ds_masked)
            ds_masked.close()

if __name__ == "__main__":

    mask_nc_with_shp(
        nc_folder, 
        shp_file, 
        output_folder,
        invert=True   # True=陆地NaN, False=陆地保留
    )

