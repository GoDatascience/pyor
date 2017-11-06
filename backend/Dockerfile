ARG BASE_IMAGE
FROM $BASE_IMAGE

MAINTAINER fernandocamargoti <fernando.camargo.ti@gmail.com>

# Install all OS dependencies for fully functional Python (scipy) and R
RUN apt-get update && apt-get -yq dist-upgrade \
 && apt-get install -yq --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    fonts-liberation \
    build-essential \
    nano \
    inkscape \
    jed \
    libsm6 \
    libxext-dev \
    libxrender1 \
    lmodern \
    pandoc \
    python-dev \
    fonts-dejavu \
    gfortran \
    gcc \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.16.1/tini && \
    echo "c7faf940a2e5234bf9e324861469d7879c44c7152555e8b143f2b7c38c3d2efc *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

# Configure general environment
ENV MINICONDA_VERSION=4.3.30 \
    MINICONDA_CHECKSUM=0b80a152332a4ce5250f3c09589c7a81 \
    CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

# Add conda to PATH
ENV PATH=$CONDA_DIR/bin:$PATH

# Install Miniconda
RUN cd /tmp && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    echo "${MINICONDA_CHECKSUM} *Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    conda update --all --yes && \
    conda clean -tipsy

# Configure Pyor environment
ENV PYOR_BACKEND=/opt/pyor/backend \
    PYOR_DATA=/var/pyor \
    PYOR_RUN=/var/run/pyor \
    PYOR_LOG=/var/log/pyor \
    PYOR_ENV_NAME=pyor \
    PYOR_ENV=/opt/conda/envs/pyor

# Activate the pyor environment
ENV PATH=$PYOR_ENV/bin:$PATH

# Create dirs
RUN mkdir -p $PYOR_BACKEND && \
    mkdir -p $PYOR_DATA && \
    mkdir -p $PYOR_RUN && \
    mkdir -p $PYOR_LOG

WORKDIR $PYOR_BACKEND

ENTRYPOINT ["tini", "--"]
CMD python manage.py runserver