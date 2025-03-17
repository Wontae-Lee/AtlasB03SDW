import os
import subprocess

from src.runner.parallel.parallel import Parallel
from src.utility.private_helpers import find_gmsh_path, find_hopr_path, find_piclas_path, find_piclas2vtk_path


class Runner:

    def __init__(self,
                 directory_path: str,
                 parallel: int = None):
        self.directory_path = directory_path
        self._gmsh = find_gmsh_path()
        self._hopr = find_hopr_path()
        self._piclas = find_piclas_path()
        self._piclas2vtk = find_piclas2vtk_path()

        if parallel is None:
            self._parallel = Parallel().physical_cores
        else:
            self._parallel = parallel

    def run(self,
            HOPR: bool = False,
            PICLAS: bool = False,
            PICLAS2VTK: bool = False):

        if HOPR:
            # Run HOPR
            subprocess.call(f"cd {self.directory_path} && {self._hopr} hopr.ini | tee hopr.log", shell=True)

        if PICLAS:
            # Run PICLAS
            subprocess.call(
                f"cd {self.directory_path} && mpirun -np {self._parallel}  {self._piclas} parameter.ini | tee piclas.log",
                shell=True)
        if PICLAS2VTK:
            # h5 files except mesh.h5
            h5_files = self._find_h5files(self.directory_path)

            for h5_file in h5_files:
                subprocess.call(
                    f"cd {self.directory_path} && {self._piclas2vtk} parameter.ini {h5_file} | tee piclas2vtk.log",
                    shell=True)

    def rerun(self, h5_file: str):
        subprocess.call(
            f"cd {self.directory_path} && mpirun -np {self._parallel}  {self._piclas} parameter.ini {h5_file} | tee piclas.log",
            shell=True)

    @staticmethod
    def _find_h5files(directory_path: str):
        dsmc_state_files = [f'{file}' for file in os.listdir(directory_path) if
                            'DSMCState' in file and file.endswith('.h5')]
        dsmc_state_files.sort()

        return dsmc_state_files
