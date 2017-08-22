FROM nvidia/cuda:8.0-cudnn7-devel

MAINTAINER fernandocamargoti <fernando.camargo.ti@gmail.com>

RUN apt-get update && \
    apt-get install -y curl build-essential libpng12-dev libffi-dev supervisor && \
    apt-get clean && \
    rm -rf /var/tmp /tmp /var/lib/apt/lists/*

RUN curl -sSL -o miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.3.21-Linux-x86_64.sh && \
    /bin/bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

ENV PATH=/opt/conda/bin:$PATH

# Use the environment.yml to create the conda environment.
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml -n mreq

ENV MREQ_BACKEND=/opt/mreq/backend \
    MREQ_DATA=/var/mreq \
    MREQ_ENV=/opt/conda/envs/mreq \
    SUPERVISOR_ENABLED=True

ENV PATH=$MREQ_ENV/bin:$PATH

ADD supervisord.conf /tmp/supervisord/supervisord.conf
ADD append_workers_to_supervisord.py /tmp/supervisord/append_workers_to_supervisord.py
ADD workers /tmp/supervisord/workers

WORKDIR /tmp/supervisord
RUN python append_workers_to_supervisord.py > /etc/supervisor/conf.d/supervisord.conf

WORKDIR /root
RUN rm -r /tmp/supervisord

VOLUME ["$MREQ_BACKEND", "$MREQ_DATA"]

# Flask and Dashboard
EXPOSE 5000 5555

CMD [ "/usr/bin/supervisord" ]
