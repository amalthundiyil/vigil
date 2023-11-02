FROM python:3.9

WORKDIR /code

COPY . /code

RUN pip install "git+https://github.com/amal-thundiyil/vigil.git@main#egg=vigil-core&subdirectory=vigil/core" && pip install . 


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

