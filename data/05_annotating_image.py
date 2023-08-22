
"""
annotating collapsed building on images

rasterio.transform.rolcol(meta['transform'], xs=x_coord, ys=y_coord)
"""

import rasterio
import os
from matplotlib import pyplot as plt
from tqdm import tqdm
from matplotlib import image
import geojson

if __name__ == "__main__":


    with open("./collapsed_building_point_example.geojson") as f:
        gj = geojson.load(f)
    features = gj['features']

    output = "collapsed_label_png_test"
    if not os.path.exists(output):
        os.makedirs(output)

    dataset = rasterio.open('after_earthquake_example.tif')
    transform = dataset.transform
    
    # annotating collapsed building on images
    for index, feature in enumerate(tqdm(features)):
        coord = feature["geometry"]['coordinates']
        row, col = rasterio.transform.rowcol(transform, coord[0], coord[1])
        k_i = (row//224)*224
        k_j = (col//224)*224
        # print(coord,k_i,k_j)

        data = image.imread(f'collapsed_png/after_{k_i}_{k_j}_{index}.png')
        plt.figure()
        plt.plot(col-k_j, row-k_i, marker="o", color="red")
        plt.imshow(data)
        plt.axis('off')
        plt.savefig(f"{output}/after_{k_i}_{k_j}_{index}.png", bbox_inches='tight', pad_inches = 0)