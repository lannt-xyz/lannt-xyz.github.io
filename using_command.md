# Docker introduction

## Một số lệnh cơ bản

### docker image

+ build docker image
  ```shell
  $ docker build -t abc:xyz . ## acb: image name, xyz: image tag
  ```
+ push docker image
  ```shell
  $ docker push lannt/abc:xyz
  ```
+ pull docker image
  ```shell
  $ docker pull lannt/abc:xyz
  ```
+ list các images ở máy local
  ```shell
  $ docker images
  ```
+ xóa docker image
  - xóa 1 image
    ```shell
    $ docker rmi lannt/abc:xyz ## image name or id
    ```
  - **xóa toàn bộ**
    ```shell
    $ docker image prune ## and then press y to proceed to remove the entire image at the local machine
    ```

### docker container

+ start container
  ```shell
  $ docker run lannt/abc:xyz
  ```
+ stop container
  ```shell
  $ docker stop 838f5afe6dbf ## container's id or name
  ```
+ xem các container đang chạy
  ```shell
  $ docker ps
  ```
+ access vào container đang chạy
  ```shell
  $ docker exec -it 838f5afe6dbf bash ## 'bash' can be changed to 'sh' depending on the os kernel
  ```

### docker compose

+ notes:
  + khi sử dụng `docker-compose` thì phải chuẩn bị trước file config với YAML format(.yml)
  + thêm options `-f` để chỉ định file YAML (trường hợp có nhiều file YAML trong cùng folder hoặc tên file YAML khác `docker-compose.yml`)

+ start tất cả service định nghĩa trong YAML file
  ```shell
  $ docker-compose up
  ```
  - thêm flag `-d` để chạy với mode `detached`
+ stop tất cả service định nghĩa trong YAML file
  ```shell
  $ docker-compose down
  ```
+ restart tất cả service định nghĩa trong YAML file
  ```shell
  $ docker-compose restart
  ```

## quick sample

### create your app

#### file structure

```sh
quick_sample
|_ app.py
|_ requirements.txt
|_ Dockerfile
|_ docker-compose.yml
```

#### file detail

```python
# app.py

import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```

```python
# requirements.txt
flask
redis
```

### create Dockerfile

```sh
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]
```

### create docker-compose.yml

```sh
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
  redis:
    image: "redis:alpine"
```

## build and run your app

```sh
$ docker-compose up -d
```

```sh
$ docker ps
```
