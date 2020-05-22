#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then

  # Install conda and the awherepy environment
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
  bash ~/miniconda.sh -b -p $HOME/miniconda
  export PATH="$HOME/miniconda/bin:$PATH"
  echo "conda activate base" >> ~/.bashrc
  source $HOME/miniconda/bin/activate
  conda config --set always_yes yes --set show_channel_urls true --set changeps1 no
  conda update -q conda
  conda config --add channels conda-forge
  conda info -a
  conda init bash
  conda env create -f environment.yml
  conda activate awhere-python
  python setup.py install
  pip install -r requirements-dev.txt
else
  sudo apt-add-repository ppa:ubuntugis/ubuntugis-unstable --yes
  sudo apt-get update
  sudo apt-get install -y libspatialindex-dev libgdal-dev python3-tk
  pip install tox-travis
fi
