import os


def atlas_directory():
    return f"{os.path.dirname(os.getcwd())}/ATLAS"


def main():
    install_sh = f"""\
#!/bin/bash
    
# Install OpenMPI
cd {atlas_directory()}
wget 'https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.3.tar.gz' -P ./external/ompi
cd ./external/ompi
tar -xf openmpi-5.0.3.tar.gz
cd openmpi-5.0.3/
./configure --prefix={atlas_directory()}/external/ompi
make all install

# OpenMPI environment Variables
export MPI_DIR={atlas_directory()}/external/ompi
export PATH="{atlas_directory()}/external/ompi/bin:$PATH"
export LD_LIBRARY_PATH="{atlas_directory()}/external/ompi/lib:$LD_LIBRARY_PATH"

# Install HOPR
cd {atlas_directory()}/external/hopr
mkdir -p build && cd build
cmake .. -DLIBS_USE_CGNS=OFF
make -j4
make install

# Install piclas
cd {atlas_directory()}/external/piclas
mkdir -p build && cd build
cmake -DPICLAS_TIMEDISCMETHOD=DSMC ..
make -j4
make install

# Install Gmsh
cd {atlas_directory()}
wget 'https://gmsh.info/bin/Linux/gmsh-4.13.0-Linux64.tgz' -P ./external/gmsh
cd ./external/gmsh
tar -xf gmsh-4.13.0-Linux64.tgz

# Install Paraview
mkdir -p {atlas_directory()}/external/paraview
cd {atlas_directory()}/external/paraview
wget -O 'ParaView-5.12.1-MPI-Linux-Python3.10-x86_64.tar.gz' \
'https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=\
v5.12&type=binary&os=Linux&downloadFile=ParaView-5.12.1-MPI-Linux-Python3.10-x86_64.tar.gz'
tar -xf ParaView-5.12.1-MPI-Linux-Python3.10-x86_64.tar.gz

"""

    with open(f"{atlas_directory()}/doc/installation/install.sh", "w") as file:
        file.write(install_sh)

    print("Installation script created successfully.")

    bashrc = f"""\

# OpenMPI environment Variables
export MPI_DIR={atlas_directory()}/external/ompi
export PATH="{atlas_directory()}/external/ompi/bin:$PATH"
export LD_LIBRARY_PATH="{atlas_directory()}/external/ompi/lib:$LD_LIBRARY_PATH"

# HOPR environment variables settings
export hopr={atlas_directory()}/external/hopr/build/bin/hopr
alias hopr='{atlas_directory()}/external/hopr/build/bin/hopr'

# piclas environment variables settings
export piclas={atlas_directory()}/external/piclas/build/bin/piclas
alias piclas='{atlas_directory()}/external/piclas/build/bin/piclas'
export piclas2vtk={atlas_directory()}/external/piclas/build/bin/piclas2vtk
alias piclas2vtk='{atlas_directory()}/external/piclas/build/bin/piclas2vtk'

# Gmsh environment variables settings
export gmsh={atlas_directory()}/external/gmsh/gmsh-4.13.0-Linux64/bin/gmsh
alias gmsh='{atlas_directory()}/external/gmsh/gmsh-4.13.0-Linux64/bin/gmsh'

# Paraview environment variables settings
export paraview={atlas_directory()}/external/paraview/ParaView-5.12.1-MPI-Linux-Python3.10-x86_64/bin/paraview
alias paraview='{atlas_directory()}/external/paraview/ParaView-5.12.1-MPI-Linux-Python3.10-x86_64/bin/paraview'
"""

    with open(f"{atlas_directory()}/etc/bashrc", "w") as file:
        file.write(bashrc)

    print("Installation script and bashrc file created successfully.")

    return 0


if __name__ == "__main__":
    main()
