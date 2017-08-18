FROM frolvlad/alpine-glibc:latest

MAINTAINER fernandocamargoti <fernando.camargo.ti@gmail.com>

ENV PATH=/opt/conda/bin:$PATH \
    ANACONDA=Anaconda3-4.4.0-Linux-x86_64.sh \
    MREQ_BACKEND=/opt/mreq/backend \
    MREQ_DATA=/var/mreq

RUN apk add --no-cache --virtual=build-deps --update-cache gcc musl-dev linux-headers \
    wget bash \
    && wget -q --no-check-certificate https://repo.continuum.io/archive/$ANACONDA \
    && /bin/bash $ANACONDA -b -p /opt/conda \
    && rm $ANACONDA

ADD ./environment.yml .
RUN conda env update

WORKDIR $MREQ_BACKEND

VOLUME ["$MREQ_BACKEND", "$MREQ_DATA"]

# Flask and Dashboard
EXPOSE 5000 5555

CMD python manage.py runserver