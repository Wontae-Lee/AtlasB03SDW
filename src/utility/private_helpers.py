import os


def find_atlas_root_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def find_gmsh_path():
    return f"{find_atlas_root_dir()}/external/gmsh/gmsh-4.13.0-Linux64/bin/gmsh"


def find_hopr_path():
    return f"{find_atlas_root_dir()}/external/hopr/build/bin/hopr"


def find_piclas_path():
    return f"{find_atlas_root_dir()}/external/piclas/build/bin/piclas"


def find_piclas2vtk_path():
    return f"{find_atlas_root_dir()}/external/piclas/build/bin/piclas2vtk"
