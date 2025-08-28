# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 17:17:39 2025

@author: 杨汉全210
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import os

filename = r"F:\wind_power\wind_202112_power.nc"

# 打开 nc 文件
ds = xr.open_dataset(filename)

# 假设变量名分别是 u10, v10, wind_direction
u10 = ds['u10'].values.flatten()
v10 = ds['v10'].values.flatten()
wind_dir = ds['wind_direction'].values.flatten()

# 如果 nc 里没有 wind_speed，可以由 u,v 计算
wind_speed = np.sqrt(u10**2 + v10**2)

# 创建风玫瑰坐标轴
fig = plt.figure(figsize=(8, 6))
ax = WindroseAxes.from_ax(fig=fig)
ax.bar(wind_dir, wind_speed, normed=True, opening=0.8, edgecolor='white',
       bins=[0, 4, 8, 16, 20])
# 设置30度分隔
ax.set_thetagrids(np.arange(360, 0, -30), labels=[
    
    "E", "ESE",  "SSE",
    "S", "SSW",  "WSW",
    "W", "WNW",  "NNW",
    "N", "NNE",  "ENE",
])

ax.set_rticks([0, 4, 8, 16, 20, 24])
# ax.set_rlabel_position(-22.5)  # 标签位置，可调整
ax.set_rmax(24)
ax.set_yticks([0, 4, 8, 16, 20, 24])
ax.set_yticklabels([str(i) for i in [0, 4, 8, 16, 20, 24]])


# 设置标签和标题
ax.set_legend(title="Wind speed (m/s)")
plt.title("Wind Rose from nc data")
plt.show()

