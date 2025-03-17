# ATLAS - B03 project
# Satellite Design Workshop

# Quick Start

## Installation PICLAS and Prerequisites

The details of the installation process are on the [README.md](./doc/installation/README.md) file.

### 1. Update and upgrade the system

```shell
sudo apt-get update
sudo apt-get upgrade
```

### 2. Prerequisites

```shell
sudo apt-get install -y git cmake build-essential ninja-build libtbb-dev gdb pkg-config python3-dev python3-pip gfortran mpich libatlas-base-dev petsc-dev libgl1-mesa-dev libxt-dev libqt5x11extras5-dev libqt5help5 qttools5-dev qtxmlpatterns5-dev-tools libqt5svg5-dev python3-numpy libopenmpi-dev qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools libxft2 
```

and/or additional packages for the documentation:

```shell
sudo apt-get install -y doxygen graphviz
```

### 3. Clone the ATLAS project

```shell
git clone https://github.com/Wontae-Lee/AtlasB03SDW.git
git submodule init 
git submodule update
```

### 4. Create a virtual environment and download the required packages

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5. Run the installation script

```shell
python3 scripts/install.py
sh doc/installation/install.sh
```

### 6. Set the environment variables

```shell
source ./your/path/to/ATLAS/etc/bashrc
```

or (preferably) add the following line to your `.bashrc` file:

```shell
alias ATLAS='source ./your/path/to/ATLAS/etc/bashrc'
```

