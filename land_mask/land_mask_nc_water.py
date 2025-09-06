# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 15:35:20 2025

@author: 杨汉全210
"""
import os
import xarray as xr
import geopandas as gpd
import numpy as np
from shapely.geometry import Point

nc_folder = r"F:\water_para"
shp_file = r"E:/AAAAA/HQD/land_mask/FAB_final_land_mask.shp"
output_folder = r"F:\water_para_masked"
os.makedirs(output_folder, exist_ok=True)

gdf = gpd.read_file(shp_file)

def mask_nc_with_shp(nc_folder, gdf, output_folder, invert=False):
    for fname in os.listdir(nc_folder):
        if not fname.endswith(".nc"):
            continue
        in_path = os.path.join(nc_folder, fname)
        out_path = os.path.join(output_folder, fname.replace(".nc", "_masked.nc"))
        
        ds = xr.open_dataset(in_path)
        masked_vars = {}

        x = ds['xgrid'].values
        y = ds['ygrid'].values

        # 创建掩膜矩阵
        mask = np.zeros_like(x, dtype=bool)
        for geom in gdf.geometry:
            # 用矢量化方法判断每个点是否在多边形内
            mask |= np.array([[geom.contains(Point(x[i,j], y[i,j])) for j in range(x.shape[1])] for i in range(x.shape[0])])
        if invert:
            mask = ~mask

        # 对每个变量掩膜
        for var_name in ds.data_vars:
            da = ds[var_name]
            if 'y' in da.dims and 'x' in da.dims:
                if 'z' in da.dims:
                    mask_3d = np.broadcast_to(mask, (da.sizes['z'], da.sizes['y'], da.sizes['x']))
                    da_masked = da.where(mask_3d)
                else:
                    da_masked = da.where(mask)
                masked_vars[var_name] = da_masked
            else:
                masked_vars[var_name] = da

        ds_masked = xr.Dataset(masked_vars)
        for c in ds.coords:
            ds_masked[c] = ds[c]

        ds_masked.to_netcdf(out_path)
        print(f"已保存: {out_path}")
        ds.close()
        ds_masked.close()

mask_nc_with_shp(nc_folder, gdf, output_folder, invert=True)
