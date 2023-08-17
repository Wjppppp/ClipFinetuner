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

To freeze dependencies 
```
pip freeze > requirements.txt
```

### Docer
```
docker build . -t finetuner:<TAG>
docker run -it --gpus all --name finetuner -p 8888:8888 -p 6006:6006 --mount type=bind,source="$(pwd)",target=/app finetuner:<TAG>

jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --debug
```