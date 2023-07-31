## Build

```
docker build . -t finetuner:<TAG>
docker run -it --gpus all --name finetuner -p 8888:8888 -p 6006:6006 --mount type=bind,source="$(pwd)",target=/app finetuner:<TAG>

jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --debug
```