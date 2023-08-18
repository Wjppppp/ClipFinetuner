""" 
This demonstrates how to use the image.h5 file
together with the index file keypoints.h5

to write images to png subfolder
"""


import contextlib
import os
import h5py
from imageio import imwrite
from tqdm import tqdm

class cfg:
   step=224

if __name__ == "__main__":
   
   # png folder
   with contextlib.suppress(FileExistsError):
      os.makedirs("after_png")

   # image h5
   image = h5py.File("after_earthquake_example.h5")
   # keypoints h5
   keypoints = h5py.File("after_earthquake_example-keypoints.h5")

   for dsname in keypoints:
      print(keypoints[dsname])
      for i,j in tqdm(keypoints[dsname][:]):
         imagename = "-".join(dsname.split("-")[:-1])
         img = image[imagename][slice(i, i + cfg.step),slice(j, j + cfg.step),:]

         if (img.shape == (cfg.step,cfg.step,3)):
            imwrite(f"after_png/after_{i}_{j}.png",img)