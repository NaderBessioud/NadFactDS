from python:3.9.12-slim-buster
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    default-libmysqlclient-dev \
    gcc \
    libpq-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*
WORKDIR / 
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY . /
CMD ["python" , "main.py" ]
