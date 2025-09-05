# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 10:20:44 2025

@author: 杨汉全210
"""

import xarray as xr
import numpy as np
import os

infile = r"F:\wind_power\yearly_mean_only\wind_2021_power_mean.nc"
outfile = r"F:\wind_power\yearly_mean_only\wind_2021_power_mean_005deg.nc"
    
    
def regrid_to_005deg(input_nc, output_nc, compress=True):
    """
    读取 NetCDF 文件并进行 0.05° 空间插值，保存为新文件

    参数
    ----
    input_nc : str
        输入文件路径
    output_nc : str
        输出文件路径
    compress : bool
        是否压缩输出
    """

    # 读取文件
    ds = xr.open_dataset(input_nc)

    # 构造新的经纬度格点 (0.05°分辨率)
    new_lon = np.arange(float(ds.lon.min()), float(ds.lon.max()) + 0.05, 0.05)
    new_lat = np.arange(float(ds.lat.min()), float(ds.lat.max()) + 0.05, 0.05)

    # 插值
    ds_interp = ds.interp(lon=new_lon, lat=new_lat, method="linear")

    # 压缩设置
    if compress:
        encoding = {var: {"zlib": True, "complevel": 4} for var in ds_interp.data_vars}
    else:
        encoding = None

    # 保存
    ds_interp.to_netcdf(output_nc, format="NETCDF4", engine="netcdf4", encoding=encoding)

    print(f"✅ 插值完成: {output_nc}")
    print(f"   原始分辨率: {float(ds.lon[1]-ds.lon[0]):.2f}° × {float(ds.lat[0]-ds.lat[1]):.2f}°")
    print(f"   新分辨率: 0.05° × 0.05°")


# 使用示例
if __name__ == "__main__":
    regrid_to_005deg(infile, outfile)
