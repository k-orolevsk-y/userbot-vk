#!/bin/bash
while :
do
    echo 'Automatic updating system and installation of python3.10 and required modules.'
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3 python3-pip software-properties-common -y
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt install python3.10 python3.10-distutils imagemagick ffmpeg -y
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
    python3.10 -m pip install --upgrade pip --quiet
    pip3.10 install --upgrade pip --quiet
    python3.10 install_modules.py
    python3.10 main.py
    echo "Waiting before restarting"
    sleep 3
done