"""
Find keypoint of sample images within which collapsed building

rasterio.transform.rolcol(meta['transform'], xs=x_coord, ys=y_coord)
"""

import os
import geojson
import rasterio
import h5py
import numpy as np
from tqdm import tqdm

class cfg:
    step = 224

if __name__ == "__main__":

    raster = rasterio.open('after_earthquake_example.tif')
    transform = raster.transform

    with open("./collapsed_building_point_example.geojson") as f:
        gj = geojson.load(f)
    features = gj['features']

    keypoints = []
    ref_list = []

    # find collapsed keypoints
    f = open("keypoints.dat","w")
    for feature in tqdm(features):

        coord = feature["geometry"]["coordinates"]
        ref = feature["properties"]["Referans No"]
        ref_list.append(ref)

        row, col = rasterio.transform.rowcol(transform, coord[0], coord[1])

        k_i = (row//cfg.step)*cfg.step
        k_j = (col//cfg.step)*cfg.step
        
        keypoints.append([k_i, k_j])
        print(f"collapsed,{ref},{k_i},{k_j}", file=f)
    
    keypoints = np.array(keypoints)
    file = h5py.File("collapsed-keypoints.h5","w")
    file.create_dataset("after_earthquake_example-keypoints",data=keypoints)
