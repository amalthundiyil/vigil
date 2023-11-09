FROM alpine:3.14 AS scorecard-builder

WORKDIR /build
RUN wget "https://github.com/ossf/scorecard/releases/download/v4.6.0/scorecard_4.6.0_linux_amd64.tar.gz" && \
    tar -xf scorecard_4.6.0_linux_amd64.tar.gz && \
    mv scorecard-linux-amd64 /usr/local/bin/scorecard

FROM python:3.9-slim

WORKDIR /code

COPY . /code

RUN apt update && apt install git -y

RUN pip install --no-cache-dir -e "git+https://github.com/amalthundiyil/vigil.git@main#egg=vigil-core&subdirectory=vigil/core" --&& pip install --no-cache-dir . 

COPY --from=scorecard-builder /usr/local/bin/scorecard /usr/local/bin/scorecard