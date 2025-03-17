import os

from src.fluid.fluid import Fluid
from src.geometry.geometry import Geometry
from src.primitive.parser.parameter_ini import ParameterINI


class AtlasToPiclas:

    def __init__(self,
                 project_name: str,
                 directory_path: str,
                 fluid: Fluid,
                 geometry: Geometry):
        self.__dimensions = geometry.get_dimensions()
        self.__project_name = project_name
        self.__directory_path = directory_path
        self.__fluid = fluid
        self.__geometry = geometry

    def find_state_h5_file(self, time: float):

        # find the files that contains '_State_' in the name.
        h5_files = [f'{self.__directory_path}/{file}' for file in os.listdir(self.__directory_path) if
                    '_State_' in file and file.endswith('.h5')]
        h5_files.sort()
        h5_files = [file.split('/')[-1] for file in h5_files]
        h5_times = [float(file.split('_State_')[-1].split('.h5')[0]) for file in h5_files]

        # find the closest time to the given time
        closest_time = min(h5_times, key=lambda x: abs(x - time))
        closest_time_index = h5_times.index(closest_time)

        # find the state file
        state_file = h5_files[closest_time_index]

        return state_file

    def create_parameter_ini(self,
                             start_time: float,
                             end_time: float,
                             time_step: float,
                             number_of_output_files: int = 10,
                             sampling_fraction: float = 0.5):

        # Set the parameters for the piclas simulation.
        parameter_ini = ParameterINI(directory_path=self.__directory_path, new_file=True)

        # Set the parameters
        parameter_options = self.__parameter_options()
        parameter_ini.add_text(parameter_options)

        # Set the fluid options
        fluid_options = self.__fluid_options()
        parameter_ini.add_text(fluid_options)

        # Add surface fluxes
        surface_fluxes = self.__surface_fluxes()
        parameter_ini.add_text(surface_fluxes)

        # Set the geometry options
        geometry_options = self.__geometry_options()
        parameter_ini.add_text(geometry_options)

        # Set the time options
        time_options = self.__time_options(start_time=start_time,
                                           end_time=end_time,
                                           time_step=time_step,
                                           number_of_output_files=number_of_output_files,
                                           sampling_fraction=sampling_fraction)
        parameter_ini.add_text(time_options)

        # Set the DSMC options
        dsmc_options = self.__dsmc_options()
        parameter_ini.add_text(dsmc_options)

        # Set the other options
        other_options = self.__other_options()
        parameter_ini.add_text(other_options)

    def __dsmc_options(self):
        dsmc_options = f"""
!=============================================================================== !
! DSMC OPTIONS
!=============================================================================== !
UseDSMC=T
Particles-DSMC-CollisMode={self.__fluid.get_collision_model()}
Particles-DSMC-CalcSurfaceVal=T
Particles-DSMC-CalcQualityFactors=T
Particles-DSMC-UseOctree=F
Particles-DSMC-UseNearestNeighbour=T
"""
        return dsmc_options

    @staticmethod
    def __time_options(start_time: float,
                       end_time: float,
                       time_step: float,
                       number_of_output_files: int,
                       sampling_fraction: float):

        options = f"""
!=============================================================================== !
! TIME
!=============================================================================== !
!Tstart={start_time}
Tend={end_time}
ManualTimeStep={time_step}
IterDisplayStep={int(end_time / time_step / 100)}
Part-AnalyzeStep={int(end_time / time_step / 100)}
Analyze_dt={end_time / 10}
Part-TimeFracForSampling={sampling_fraction}
Particles-NumberForDSMCOutputs={number_of_output_files}
"""
        return options

    def __geometry_options(self):
        geometry_options = f"""
!=============================================================================== !
! GEOMETRY
!=============================================================================== !
Part-nBounds={self.__geometry.get_number_of_boundaries()}
!=============================================================================== !
! BOUNDARY OPTIONS
!=============================================================================== !"""
        for key, value in self.__geometry.get_boundary_options().items():
            geometry_options += f"\n{key}={value}"
        geometry_options += f"""
!=============================================================================== !
! BOUNDARY CONDITIONS
!=============================================================================== !"""

        for idx, name in enumerate(self.__geometry.get_boundary_names()):
            options = self.__geometry.get_boundary_info(name)
            for key, value in options.items():
                geometry_options += f"\nPart-Boundary{idx + 1}-{key}={value}"

        return geometry_options

    def __surface_fluxes(self):
        surface_fluxes = f"""
!=============================================================================== !
! SURFACE FLUXES
!=============================================================================== !"""
        # \TODO: Currently, the number of species is set to 1. This should be set by the user in the future.
        num_of_species = 1
        for i, surface_flux in enumerate(self.__fluid.surface_fluxes):
            surface_fluxes += f"""
!=============================================================================== !
! Boundary name: {surface_flux['BC']}
!=============================================================================== !
Part-Species{num_of_species}-SurfaceFlux{i + 1}-BC={self.__geometry.get_boundary_index(surface_flux['BC']) + 1}
Part-Species{num_of_species}-SurfaceFlux{i + 1}-velocityDistribution={surface_flux['velocityDistribution']}
Part-Species{num_of_species}-SurfaceFlux{i + 1}-MWTemperatureIC={surface_flux['MWTemperatureIC']}
Part-Species{num_of_species}-SurfaceFlux{i + 1}-TempVib={surface_flux['TempVib']}
Part-Species{num_of_species}-SurfaceFlux{i + 1}-TempRot={surface_flux['TempRot']}
Part-Species{num_of_species}-SurfaceFlux{i + 1}-VeloIC={surface_flux['VeloIC']}
Part-Species{num_of_species}-SurfaceFlux{i + 1}-VeloVecIC={surface_flux['VeloVecIC']}
Part-Species{num_of_species}-SurfaceFlux{i + 1}-Adaptive={surface_flux['Adaptive']}
Part-Species{num_of_species}-SurfaceFlux{i + 1}-Adaptive-Type={surface_flux['Adaptive-Type']}
Part-Species{num_of_species}-SurfaceFlux{i + 1}-Adaptive-Pressure={surface_flux['Adaptive-Pressure']}"""
        return surface_fluxes

    def __fluid_options(self):
        # \TODO: Currently, the number of species is set to 1. This should be set by the user in the future.
        num_of_species = 1
        fluid_options = f"""
!=============================================================================== !
! FLUID
!=============================================================================== !
!=============================================================================== !
!Properties of {self.__fluid.get_properties()['Name']}
!=============================================================================== !
Part-Species{num_of_species}-nSurfaceFluxBCs={len(self.__fluid.surface_fluxes)}
Part-Species{num_of_species}-nInits={len(self.__fluid.internal_fluxes)}
"""
        for option in self.__fluid.get_properties():
            fluid_options += f"Part-Species{num_of_species}-{option}={self.__fluid.get_properties()[option]}\n"
        fluid_options += f"Part-Species{num_of_species}-MacroParticleFactor={self.__fluid.macro_particle_factor}\n"

        return fluid_options

    def __parameter_options(self):
        return f"""
!=============================================================================== !
! PARAMETERS
!=============================================================================== !
ProjectName={self.__project_name}
MeshFile={self.__project_name}_mesh.h5
"""

    @staticmethod
    def __other_options():
        # \TODO: The options should be set by the user in the future.
        return """\
!=============================================================================== !
! DISCRETIZATION OPTIONS
!=============================================================================== !

N=1
NAnalyze=1
TrackingMethod=triatracking
CFLScale=0.2
!=============================================================================== !
! LOAD BALANCE OPTIONS
!=============================================================================== !

Particles-MPIWeight=1000
DoLoadBalance=F
UseH5IOLoadBalance=F
PartWeightLoadBalance=T
DoInitialAutoRestart=F
InitialAutoRestart-PartWeightLoadBalance=F
LoadBalanceMaxSteps=2
!=============================================================================== !
! OUTPUT OPTIONS
!=============================================================================== !

CalcSurfaceImpact=T
CalcSurfFluxInfo=T
CountNbrOfLostParts=F
Part-NumberOfRandomSeeds=2
Particles-RandomSeed1=1
Particles-RandomSeed2=2
ColoredOutput=F
TimeStampLength=13
NVisu=1
CalcPointsPerDebyeLength=F

"""
