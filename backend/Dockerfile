FROM continuumio/miniconda3

MAINTAINER fernandocamargoti <fernando.camargo.ti@gmail.com>

RUN apt-get update && apt-get install -y \
    build-essential \
    supervisor

# Use the environment.yml to create the conda environment.
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml -n mreq

ENV MREQ_BACKEND=/opt/mreq/backend \
    MREQ_DATA=/var/mreq \
    MREQ_ENV=/opt/conda/envs/mreq \
    SUPERVISOR_ENABLED=True

ENV PYTHON=$MREQ_ENV/bin/python \
    PATH=$MREQ_ENV/bin:$PATH

ADD supervisord.conf /tmp/supervisord/supervisord.conf
ADD append_workers_to_supervisord.py /tmp/supervisord/append_workers_to_supervisord.py
ADD workers /tmp/supervisord/workers

WORKDIR /tmp/supervisord
RUN $PYTHON append_workers_to_supervisord.py > /etc/supervisor/conf.d/supervisord.conf

WORKDIR /root
RUN rm -r /tmp/supervisord

VOLUME ["$MREQ_BACKEND", "$MREQ_DATA"]

# Flask and Dashboard
EXPOSE 5000 5555

CMD [ "/usr/bin/supervisord" ]
