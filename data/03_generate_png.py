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

def clip_image_from_keypoionts(image, keypoints, step, output):

   for dsname in keypoints:
      print(keypoints[dsname])
      k = 0
      for i,j in tqdm(keypoints[dsname][:]):
         imagename = "-".join(dsname.split("-")[:-1])
         img = image[imagename][slice(i, i + step),slice(j, j + step),:]

         if (img.shape == (step,step,3)):
            imwrite(f"{output}/after_{i}_{j}_{k}.png",img)
            k += 1

if __name__ == "__main__":
   
   # png folder
   output = "collapsed_png"
   if not os.path.exists(output):
      os.makedirs(output)

   # image h5
   image = h5py.File("after_earthquake_example.h5")
   # keypoints h5
   keypoints = h5py.File("collapsed-keypoints.h5")

   clip_image_from_keypoionts(image, keypoints, cfg.step, output)

   image.close()
   keypoints.close()