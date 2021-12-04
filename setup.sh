#/bin/bash
sudo apt update && sudo apt upgrade -y
sudo apt-get install build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-pip \
    zip \
    python3-picamera \
    libgtk-3-dev \
    libopenexr-dev \
    libilmbase23

sudo apt-get clean
pip3 install --upgrade picamera[array]  


pip3 install dlib face_recognition RPi.GPIO
pip3 install opencv-python==4.5.3.56



#mkdir -p dlib
#git clone -b 'v19.6' --single-branch https://github.com/davisking/dlib.git dlib/
#cd ./dlib
#sudo python3 setup.py install --compiler-flags "-mfpu=neon"

#pip3 install face_recognition

#git clone https://github.com/Itseez/opencv.git && cd opencv &&git checkout 3.0.0
#pip3 install dlib face_recognition RPi.GPIO
#pip3 install --upgrade setuptools pip
#sudo pip install opencv-python
