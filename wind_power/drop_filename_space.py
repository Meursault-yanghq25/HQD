# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 16:14:22 2025

@author: 杨汉全210
"""

import os
import glob

folder = r"F:\water_para"

# 查找所有 nc 文件
files = glob.glob(os.path.join(folder, "*.nc"))

for f in files:
    dirname = os.path.dirname(f)
    basename = os.path.basename(f)
    new_basename = basename.strip()
    new_path = os.path.join(dirname, new_basename)
    if f != new_path:
        os.rename(f, new_path)
        print(f"Renamed: '{basename}' -> '{new_basename}'")
