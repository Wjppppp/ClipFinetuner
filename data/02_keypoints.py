"""
This script takes input h5 and samples over it in 224*224 subimages
The images have no overlap

For each non-empty image tile, a vector x0,y0 is generated to be stored in a HDF5 dataset keypoints

Then, embeddings can be computed by mapping over keypoints 

key functions: compute_keypoints

"""

import h5py
import itertools
import numpy as np
from tqdm import tqdm

class cfg:
    step=224


def compute_keypoints(name, ds):
    print(f"Computing keypoints for {name}")

    keypoints = []
    f = open("keypoints.dat","w")
    plan = list(itertools.product(range(0, ds.shape[0], cfg.step),range(0, ds.shape[1], cfg.step)))

    for ((i,j)) in tqdm(plan):
        image = ds[slice(i, i + cfg.step),slice(j, j + cfg.step),:]

        if (np.mean(image) != 0):
            keypoints = keypoints + [[i,j]]
            print(f"{name},{i},{j}", file=f)

    keypoints = np.array(keypoints)
    h5py.File(f"{name}-keypoints.h5","w").create_dataset(f"{name}-keypoints",data=keypoints)


if __name__=="__main__":
    f = h5py.File("before_earthquake_example.h5")
    for dataset in f:
        compute_keypoints(dataset,f[dataset])
    