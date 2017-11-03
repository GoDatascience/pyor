ARG BASE_IMAGE
FROM $BASE_IMAGE

MAINTAINER fernandocamargoti <fernando.camargo.ti@gmail.com>

RUN apt-get update && \
    apt-get install -y curl build-essential libpng12-dev libffi-dev libxrender1 fonts-dejavu gfortran build-essential inkscape jed libsm6 libxext-dev libxrender1 lmodern pandoc python-dev&& \
    apt-get clean && \
    rm -rf /var/tmp /tmp /var/lib/apt/lists/*

RUN curl -sSL -o miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.3.21-Linux-x86_64.sh && \
    /bin/bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

ENV PATH=/opt/conda/bin:$PATH

# Use the environment.yml to create the conda environment.
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml -n pyor

ENV PYOR_BACKEND=/opt/pyor/backend \
    PYOR_DATA=/var/pyor \
    PYOR_RUN=/var/run/pyor \
    PYOR_LOG=/var/log/pyor \
    PYOR_ENV=/opt/conda/envs/pyor

RUN mkdir -p $PYOR_DATA && \
    mkdir -p $PYOR_RUN && \
    mkdir -p $PYOR_LOG

ENV PATH=$PYOR_ENV/bin:$PATH

VOLUME ["$PYOR_BACKEND", "$PYOR_DATA", "$PYOR_LOG"]

WORKDIR $PYOR_BACKEND

# Flask and Dashboard
EXPOSE 5000 5555

CMD python manage.py runserver
