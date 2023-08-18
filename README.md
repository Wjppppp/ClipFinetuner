## Build

### Venv

To build venv:

```
python -m venv venv
venv\Scripts\activate.bat
# or
venv\Scripts\activate.ps1
pip install -r requirements.txt
```

To freeze dependencies:

```
pip freeze > requirements.txt
```

### Docer
```
docker build . -t finetuner:<TAG>
docker run -it --gpus all --name finetuner -p 8888:8888 -p 6006:6006 --mount type=bind,source="$(pwd)",target=/app finetuner:<TAG>

jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --debug
```

## Dataset Preparation

Go to data folder:
`cd data`

Make sure you have tif image under `<your_project_path>/data/`.

To convert tif to hdf5:
```
python 01_tif_to_hdf5.py
```

To calculate keypoints with fixed step across the whole image:
```
python 02_keypoints,py
```

To generate png from image.h5 and keypoints.h5:
```
python 03_generate_png.py
```

**Note: Don't forget change input path before running each python script.**