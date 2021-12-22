#!/bin/bash
sudo apt update && sudo apt upgrade -y
sudo apt-get install build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-pip \
    zip \
    python3-picamera \
    libgtk-3-dev \
    libopenexr-dev \
    libilmbase23
sudo apt-get clean
