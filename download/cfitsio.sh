#!/bin/bash

# Proceso descarga e instalación de cfitsio


# Decarga de cfitsio:
wget heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-4.1.0.tar.gz

# Decomprimir cfitiso:
tar -xzvf cfitsio*.tar.gz
cd cfitsio*/

# Instalación de cfitisio:
./configure --prefix=/usr/local
sudo make
sudo make install

# Instalación de funpack
make fpack
make funpack
