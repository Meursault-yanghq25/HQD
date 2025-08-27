# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 15:41:26 2025

@author: 杨汉全210
"""

import xarray as xr
import numpy as np

def calc_wind_energy(input_nc, output_nc, rho=1.225, compress=True):
    """
    从风场文件计算风能密度和风向，并保存为新的 NetCDF 文件

    参数
    ----
    input_nc : str
        输入文件路径，必须包含变量 u10, v10 (dims: time, lon, lat)
    output_nc : str
        输出文件路径
    rho : float, optional
        空气密度 (kg/m^3)，默认 1.225
    compress : bool, optional
        是否压缩输出 NetCDF 文件，默认 True
    """

    # 读取输入数据
    ds = xr.open_dataset(input_nc)
    u10 = ds["u10"]
    v10 = ds["v10"]

    # 计算风速
    wind_speed = np.sqrt(u10**2 + v10**2)

    # 计算风能密度 (W/m²)
    wind_power_density = 0.5 * rho * wind_speed**3
    wind_power_density = wind_power_density.rename("wind_power_density")
    wind_power_density.attrs["units"] = "W m-2"
    wind_power_density.attrs["long_name"] = "Wind Power Density at 10m"

    # 计算风向 (度, 气象定义：来流方向)
    wind_direction = (270 - np.rad2deg(np.arctan2(v10, u10))) % 360
    wind_direction = wind_direction.rename("wind_direction")
    wind_direction.attrs["units"] = "degree"
    wind_direction.attrs["long_name"] = "Wind Direction (coming from, meteorological)"

    # 合并成新数据集
    ds_out = xr.Dataset(
        {
            "wind_power_density": wind_power_density,
            "wind_direction": wind_direction
        },
        coords=ds.coords
    )

    # 压缩设置
    if compress:
        encoding = {
            "wind_power_density": {"zlib": True, "complevel": 4},
            "wind_direction": {"zlib": True, "complevel": 4},
        }
    else:
        encoding = None

    # 保存结果
    ds_out.to_netcdf(output_nc, engine="netcdf4", format="NETCDF4", encoding=encoding)

    print(f"\n✅ 成功生成 {output_nc}")


# 使用示例
if __name__ == "__main__":
    calc_wind_energy("wind.nc", "wind_energy.nc")
