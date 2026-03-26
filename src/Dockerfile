FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

MAINTAINER mabuaita@yahoo.com

# Libraries and dependencies

RUN \
  apt-get update && apt-get -y install \
  libboost-thread-dev \
  libjpeg-dev \
  libopenexr-dev \
  libpng-dev \
  libtiff-dev \
  python3 \
  python3-dev \
  python-distribute \
  python3-pip \
  unzip \
  zlib1g-dev \
  vim

COPY . /

EXPOSE 8777/tcp
CMD [ "python3", "app.py" ]
#CMD [ "tail", "-f", "/dev/null" ]
