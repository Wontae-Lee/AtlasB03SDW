import os
import subprocess

from src.fluid.fluid import Fluid
from src.geometry.geometry import Geometry
from src.runner.runner import Runner
from src.transfer.atlas_to_piclas import AtlasToPiclas
from src.utility.shell_scripts import generate_scripts
from src.utility.utility import save_history


class Simulator:

    def __init__(self,
                 project_name: str,
                 directory_path: str,
                 fluid: Fluid,
                 geometry: Geometry):

        # Set the parameters
        os.makedirs(directory_path, exist_ok=True)
        self.project_name = project_name
        self._dimensions = geometry.get_dimensions()
        self.directory_path = directory_path
        self.__fluid = fluid
        self.__geometry = geometry
        generate_scripts(directory_path=directory_path)

        # Set the transfer
        self.__atlas_to_piclas = AtlasToPiclas(project_name=project_name,
                                               directory_path=directory_path,
                                               fluid=fluid,
                                               geometry=geometry)

        # Set the runner
        self.__runner = Runner(directory_path=self.directory_path)

    def run(self,
            start_time: float = 0,
            end_time: float = None,
            time_step: float = None,
            number_of_output_files: int = 10,
            sampling_fraction: float = 0.5):

        # Run HOPR
        self.__geometry.create_hopr_file(project_name=self.project_name, hopr_file_directory=f"{self.directory_path}")
        self.__runner.run(HOPR=True)

        # Transfer the data to PICLAS
        self.__atlas_to_piclas.create_parameter_ini(start_time=start_time,
                                                    end_time=end_time,
                                                    time_step=time_step,
                                                    number_of_output_files=number_of_output_files,
                                                    sampling_fraction=sampling_fraction)

        # Run PICLAS
        self.__runner.run(PICLAS=True)

    def rerun(self,
              start_time: float = 0,
              end_time: float = None,
              time_step: float = None,
              number_of_output_files: int = 10,
              sampling_fraction: float = 0.5):

        # Save the history before rerunning
        save_history(directory_path=self.directory_path, index=0, history=f'rerun_{start_time}', STATE=True)

        # Find the state file
        h5_file = self.__atlas_to_piclas.find_state_h5_file(time=start_time)

        # Transfer the data to PICLAS
        self.__atlas_to_piclas.create_parameter_ini(start_time=start_time,
                                                    end_time=end_time,
                                                    time_step=time_step,
                                                    number_of_output_files=number_of_output_files,
                                                    sampling_fraction=sampling_fraction)

        # Run PICLAS
        self.__runner.rerun(h5_file=h5_file)

    def clean(self):
        for file in os.listdir(self.directory_path):
            if ((file.endswith('.h5') and '_mesh' not in file)
                    or file.endswith('.vtu') or file.endswith('.csv')
                    or file.endswith('.tmp') or file.endswith('.dat')
                    or file.endswith('.out') or file.endswith('.log')):
                os.remove(f'{self.directory_path}/{file}')

    @staticmethod
    def shut_down():
        subprocess.call("shutdown -h now", shell=True)
