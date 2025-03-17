## Installation PICLAS and Prerequisites


### 1. Update and upgrade the system

```shell
sudo apt-get update
sudo apt-get upgrade
```

### 2. Prerequisites

```shell
sudo apt-get install -y git cmake build-essential ninja-build libtbb-dev gdb pkg-config python3-dev python3-pip gfortran mpich libatlas-base-dev petsc-dev libgl1-mesa-dev libxt-dev libqt5x11extras5-dev libqt5help5 qttools5-dev qtxmlpatterns5-dev-tools libqt5svg5-dev python3-numpy libopenmpi-dev qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools python3.10-venv libxft2 
```

### 3. Clone the ATLAS project

```shell
git clone https://github.com/Wontae-Lee/ATLAS.git
git submodule init 
git submodule update
```

### 4. Create a virtual environment and download the required packages

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5. Install the required packages

```shell
# Install OpenMPI
cd /path/to/ATLAS
wget 'https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.3.tar.gz' -P ./external/ompi
cd ./external/ompi
tar -xf openmpi-5.0.3.tar.gz
cd openmpi-5.0.3/
./configure --prefix=/path/to/ATLAS/external/ompi
make all install

# OpenMPI environment Variables
export MPI_DIR=f/path/to/ATLAS/external/ompi
export PATH="/path/to/ATLAS/external/ompi/bin:$PATH"
export LD_LIBRARY_PATH="/path/to/ATLAS/external/ompi/lib:$LD_LIBRARY_PATH"

# Install HOPR
cd /path/to/ATLAS/external/hopr
mkdir -p build && cd build
cmake .. -DLIBS_USE_CGNS=OFF
make -j4
make install

# HOPR environment variables settings
export hopr=/path/to/ATLAS/external/hopr/build/bin/hopr

# Install piclas
cd /path/to/ATLAS/external/piclas
mkdir -p build && cd build
cmake -DPICLAS_TIMEDISCMETHOD=DSMC ..
make -j4
make install

# piclas environment variables settings
export piclas=/path/to/ATLAS/external/piclas/build/bin/piclas

# Install Gmsh
cd /path/to/ATLAS
wget 'https://gmsh.info/bin/Linux/gmsh-4.13.0-Linux64.tgz' -P ./external/gmsh
cd ./external/gmsh
tar -xf gmsh-4.13.0-Linux64.tgz

# Gmsh environment variables settings
export gmsh=/path/to/ATLAS/external/gmsh/gmsh-4.13.0-Linux64/bin/gmsh

# Install Paraview
cd /path/to/ATLAS
wget -O 'ParaView-5.12.1-MPI-Linux-Python3.10-x86_64.tar.gz' 'https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.12&type=binary&os=Linux&downloadFile=ParaView-5.12.1-MPI-Linux-Python3.10-x86_64.tar.gz' -P /path/to/ATLAS/external/paraview
cd /path/to/ATLAS/external/paraview
tar -xf ParaView-5.12.1-MPI-Linux-Python3.10-x86_64.tar.gz

# Paraview environment variables settings
export paraview=/path/to/ATLAS/external/paraview/ParaView-5.12.1-MPI-Linux-Python3.10-x86_64/bin/paraview
```

### 6. Set the environment variables

```shell
source ./path/to/ATLAS/etc/bashrc
```

or (preferably) add the following line to your `.bashrc` file:

```shell
alias ATLAS='source ./path/to/ATLAS/etc/bashrc'
```

