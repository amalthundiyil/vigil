FROM python:3.8

WORKDIR /code

COPY . /code

RUN apt update && apt install git tk -y

RUN pip install --no-cache-dir -e "git+https://github.com/amal-thundiyil/vigil.git@main#egg=vigil-core&subdirectory=vigil/core" --&& pip install --no-cache-dir

