"""
This script convert tif to h5
only consider first three band as r, g, b
h5 attribute contains transform and boundary latlon of origin tif (left, bottom, right, top)
to calculate latlon from image coords:

dataset.transform * (col, row)

Author: Jiapan Wang
Date: 18.08.2023
"""

import rasterio
import numpy as np
import h5py

class cfg:
    step = 224

if __name__ == "__main__":

    file_path = 'before_earthquake_example.tif'
    file_name = file_path.split(".")[0]
    
    # raster dataset
    dataset = rasterio.open(file_path)
    red = dataset.read(1)
    green = dataset.read(2)
    blue = dataset.read(3)

    image = np.stack([red, green, blue], axis=-1)
    print(image.shape)

    # dataset.h5
    f = h5py.File(f'{file_name}.h5','w')
    f.create_dataset(file_name, data=image, chunks=(cfg.step, cfg.step, 3))

    # attribute of dataset
    f[file_name].attrs['transform'] = dataset.transform
    f[file_name].attrs['left'] = dataset.bounds.left
    f[file_name].attrs['bottom'] = dataset.bounds.bottom
    f[file_name].attrs['right'] = dataset.bounds.right
    f[file_name].attrs['top'] = dataset.bounds.top