from python:3.9.12-slim-buster
RUN apt-get update && apt-get install -y \
    cmake \
    default-libmysqlclient-dev \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR / 
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY . /
CMD ["python" , "main.py" ]
