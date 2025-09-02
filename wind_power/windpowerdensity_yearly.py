# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 19:34:51 2025

@author: 杨汉全210
"""

import os
import glob
import time
import xarray as xr
from tqdm import tqdm
import numpy as np

inputfolder = r"F:\wind_power\yearly"
outputfolder = r"F:\wind_power\yearly_mean_only"
    
    
def yearly_mean(input_file, output_file, compress=False):
    """
    Lire un fichier NetCDF, calculer les moyennes temporelles
    et sauvegarder les résultats dans un nouveau fichier.

    Paramètres
    ----------
    input_file : str
        chemin du fichier NetCDF d'entrée
    output_file : str
        chemin du fichier NetCDF de sortie
    compress : bool
        activer ou non la compression
    """
    # Lire le fichier
    ds = xr.open_dataset(input_file)

    # ---- Calculer la vitesse instantanée du vent ----
    wind_speed = np.sqrt(ds["u10"]**2 + ds["v10"]**2)
    wind_speed = wind_speed.rename("wind_speed")
    wind_speed.attrs["units"] = "m s-1"
    wind_speed.attrs["long_name"] = "Wind Speed at 10m"

    # Ajouter wind_speed au dataset
    ds = ds.assign(wind_speed=wind_speed)

    # ---- Calculer la moyenne temporelle pour chaque variable ----
    ds_mean = ds.mean(dim="time", skipna=True, keep_attrs=True)

    # Renommer les variables moyennes (ajout suffixe "_mean")
    keep_vars = ["wind_power_density", "wind_direction", "wind_speed"]
    ds_mean = ds_mean[keep_vars]
    ds_mean = ds_mean.rename({var: var + "_mean" for var in ds_mean.data_vars})

    # Fusionner original + moyennes
    # ds_out = xr.merge([ds, ds_mean])
    ds_out = xr.merge([ds_mean])
    # Encodage pour compression
    if compress:
        encoding = {var: {"zlib": True, "complevel": 4} for var in ds_out.data_vars}
    else:
        encoding = None

    # Sauvegarde
    ds_out.to_netcdf(output_file, format="NETCDF4", engine="netcdf4", encoding=encoding)


if __name__ == "__main__":
    os.makedirs(outputfolder, exist_ok=True)

    inputfiles = glob.glob(os.path.join(inputfolder, "*.nc"))
    names = [os.path.splitext(os.path.basename(f))[0] for f in inputfiles]
    outputfiles = [os.path.join(outputfolder, name + "_mean.nc") for name in names]

    start_time = time.time()
    print("\nDébut du processus!\n")
    print("-" * 50)

    for infile, outfile in tqdm(zip(inputfiles, outputfiles),
                                total=len(inputfiles),
                                desc="Traitement des fichiers",
                                unit="fichier"):
        # Vérifier si le fichier existe déjà
        if os.path.exists(outfile):
            print(f"⚠️  Fichier déjà existant, sauté : {outfile}")
            continue

        yearly_mean(infile, outfile)
    
    if inputfiles:
        last_file = inputfiles[-1]
        print("\nLast input file information:")
        print(f"File: {last_file}")
        ds_example = xr.open_dataset(last_file)
        print(ds_example.time)
        print(ds_example)
        ds_example.close()

    if outputfiles:
        last_file = outputfiles[-1]
        print("\nLast output file information:")
        print(f"File: {last_file}")
        ds_example = xr.open_dataset(last_file)
        # print(ds_example.time)
        print(ds_example)
        ds_example.close()
        
        
    end_time = time.time()
    elapsed = end_time - start_time

    heures = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    secondes = elapsed % 60

    print("\n" + "-" * 50)
    print("\n✅ Processus terminé!\n")
    print(f"⏱️ Temps total : {heures}h {minutes}m {secondes:.2f}s")
