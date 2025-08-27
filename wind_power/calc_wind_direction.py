# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 16:25:24 2025

@author: 杨汉全210
"""

import numpy as np

def calc_wind_direction(u, v):
    theta = (270 - np.rad2deg(np.arctan2(v, u))) % 360
    return theta

# 例子
u = np.array([0, 1, 0, -1, 1])
v = np.array([1, 0, -1, 0, 1])

wind_dir = calc_wind_direction(u, v)
print(wind_dir)  # 输出: [  0.  90. 180. 270.  45.]
