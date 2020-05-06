FROM python:3.8.2-alpine as builder


RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk update
RUN apk add --upgrade apk-tools

RUN apk add \
    --update alpine-sdk

RUN apk add openssl \
    ca-certificates \
    libxml2-dev \
    postgresql-dev \
    jpeg-dev \
    libffi-dev \
    linux-headers \
    python3-dev \
    libxslt-dev \
    xmlsec-dev


RUN apk add --update-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing/ \
    gcc \
    g++

RUN pip install --upgrade \
    setuptools \
    pip \
    wheel \
    pipenv

WORKDIR /nomenklatura/
ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --system  --ignore-pipfile --deploy


FROM python:3.8.2-alpine

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN apk update
RUN apk add --upgrade apk-tools
RUN apk add postgresql-client \
    openssl \
    ca-certificates \
    libxml2-dev \
    jpeg \
    nodejs-npm \
    git


ADD contrib/*.sh /usr/local/bin/
WORKDIR /var/nomenklatura

ADD package.json .
ADD package-lock.json .
RUN npm install install

ADD . /code/
WORKDIR /code/

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code

ENTRYPOINT ["entrypoint.sh"]
RUN ["chmod", "+x", "/usr/local/bin/entrypoint.sh"]

EXPOSE 8000
