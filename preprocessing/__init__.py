import os

# Raw data
PATH_RAW = "./raw"
# PATH_RAW_BEFORE_TIF = os.path.join(PATH_RAW, "before_example.tif")
# PATH_RAW_AFTER_TIF = os.path.join(PATH_RAW, "after_example.tif")

# Temporary data
PATH_TMP = "./tmp"
PATH_TMP_H5 = os.path.join(PATH_TMP, "h5")
PATH_TMP_PNG = os.path.join(PATH_TMP, "png")
PATH_TMP_BOUND = os.path.join(PATH_TMP, "bound")

try:
   os.makedirs(PATH_TMP_H5)
   os.makedirs(PATH_TMP_PNG)
   os.makedirs(PATH_TMP_BOUND)
except FileExistsError:
   pass



# tile attr
TILE_W = 112
TILE_H = 112
STEP = 112
