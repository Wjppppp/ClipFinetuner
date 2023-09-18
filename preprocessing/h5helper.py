from . import *
import rasterio
import numpy as np
import h5py
from tqdm import tqdm
import itertools
from imageio import imwrite
from geojson import Polygon, Feature, FeatureCollection, dump
from affine import Affine

def tif2hdf5(h5_name):
    """
    Store multiple tif images into hdf5
    """
    for fname in os.listdir(PATH_RAW):
        if fname.endswith("tif"):

            tif_name = fname.split(".")[0]

            # raster dataset
            tif_path = os.path.join(PATH_RAW, fname)
            dataset = rasterio.open(tif_path)
            red = dataset.read(1)
            green = dataset.read(2)
            blue = dataset.read(3)

            image = np.stack([red, green, blue], axis=-1)
            print(f"The image size of {tif_name} is: {image.shape}")

            # create h5
            h5_path = os.path.join(PATH_TMP_H5, f'{h5_name}.h5')
            if not os.path.exists(h5_path):
                f = h5py.File(h5_path, "w")
            else:
                f = h5py.File(h5_path, "r+")

            if tif_name in f.keys():
                continue
            f.create_dataset(tif_name, data=image, chunks=(STEP, STEP, 3))

            # attribute of dataset
            f[tif_name].attrs['transform'] = dataset.transform
            f[tif_name].attrs['left'] = dataset.bounds.left
            f[tif_name].attrs['bottom'] = dataset.bounds.bottom
            f[tif_name].attrs['right'] = dataset.bounds.right
            f[tif_name].attrs['top'] = dataset.bounds.top

    print(f.keys())
    f.close()
    return


def compute_keypoints(h5_name):
    """
    compute keypoints
    """

    input_path = os.path.join(PATH_TMP_H5, f'{h5_name}.h5')
    f1 = h5py.File(input_path, "r")

    for ds_name in f1:
        ds=f1[ds_name]
        print(f"Computing keypoints for {ds_name}")

        keypoints = []
        # f = open("keypoints.dat", "w")
        plan = list(itertools.product(range(0, ds.shape[0], TILE_H), range(0, ds.shape[1], TILE_W)))

        for ((i, j)) in tqdm(plan):
            image = ds[slice(i, i + TILE_H), slice(j, j + TILE_W), :]

            if (np.mean(image) != 0):
                keypoints = keypoints + [[i, j]]
                # print(f"{ds},{i},{j}", file=f)

        keypoints = np.array(keypoints)

        # create keypoints h5
        output_path = os.path.join(PATH_TMP_H5, f'{h5_name}-keypoints.h5')
        if not os.path.exists(output_path):
            f2 = h5py.File(output_path, "w")
        else:
            f2 = h5py.File(output_path,"r+")

        if f"{ds_name}-keypoints" in f2.keys():
            continue
        f2.create_dataset(f"{ds_name}-keypoints", data=keypoints)

    print(f2.keys())
    f1.close()
    f2.close()
    return


def clip_image_from_keypoionts(image, keypoints, transform, step_i, step_j, ds_name):
    """
    clip image from keypoints into tiles and geojson bound
    """
    print(keypoints.shape)
    k = 0
    features = [] # bound geojson object list

    for i,j in tqdm(keypoints[:]):
        img = image[slice(i, i + step_i),slice(j, j + step_j),:]

        if (img.shape == (step_i,step_j,3)):

            # png folder
            output = os.path.join(PATH_TMP_PNG, ds_name)
            if not os.path.exists(output):
                os.makedirs(output)

            out_image = os.path.join(output, f"{i}_{j}.png")
            imwrite(out_image,img)

            polygon = transform_polygon(transform, i, j, step_i, step_j)
            properties = {
                "keypoints":(int(i),int(j)),
                "path":out_image,
                "label":ds_name
                }
            features.append(Feature(
                geometry=polygon,
                properties=properties
            ))
            k+=1
    print(f"{k} images generated!")

    # geojson folder
    feature_collection = FeatureCollection(features)
    geojson_dir = f"{PATH_TMP_BOUND}/{ds_name}"

    if not os.path.exists(geojson_dir):
        os.makedirs(geojson_dir)

    with open(f"{geojson_dir}/bound.geojson", 'w') as f:
        dump(feature_collection, f)

def transform_polygon(transform, i, j, step_i, step_j):
    """
    transform image pixel to lon,lat coords based on AffineTransformer.
    """

    affine = transform
    transformer = rasterio.transform.AffineTransformer(Affine(affine[0],affine[1],affine[2],affine[3],affine[4],affine[5]))

    (x1, y1) = transformer.xy(i, j)
    (x2, y2) = transformer.xy(i, j + step_j)
    (x3, y3) = transformer.xy(i + step_i, j + step_j)
    (x4, y4) = transformer.xy(i + step_i, j)

    return Polygon([[(x1,y1), (x2,y2), (x3,y3), (x4,y4), (x1,y1)]])

def generate_png(h5_name):
    """
    generate png samples
    """    
    # image h5
    image_h5 = h5py.File(f"{PATH_TMP_H5}/{h5_name}.h5","r")
    # keypoints h5
    keypoints_h5 = h5py.File(f"{PATH_TMP_H5}/{h5_name}-keypoints.h5","r")

    for ds_name in image_h5:
        print(f"Generating sample images for {ds_name}.")
        image = image_h5[ds_name]
        transform = image_h5[ds_name].attrs['transform']

        if keypoints := keypoints_h5[f'{ds_name}-keypoints']:
            clip_image_from_keypoionts(image, keypoints, transform, TILE_H, TILE_W, ds_name)
        else:
            print(f"Can not find keypoints for {ds_name}.")

    image_h5.close()
    keypoints_h5.close()
    return
