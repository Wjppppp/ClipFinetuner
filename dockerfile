FROM python:3.8

RUN apt-get update &&\
    apt-get install -y \
    git

RUN python -m pip install --upgrade pip

# finetuner-full will install ML libraries such as torchvision and transformers
RUN pip install -U "finetuner[full]" 
RUN pip install gdown
RUN pip install git+https://github.com/openai/CLIP.git
RUN pip install notebook
RUN pip install ipywidgets

WORKDIR /app
COPY . .

CMD [ "bash" ]