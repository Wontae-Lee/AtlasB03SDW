import abc
import json

import numpy as np

from src.utility.private_helpers import find_atlas_root_dir


# Abstract class for all particles
class Fluid:

    def __init__(self, collision_model: str, macro_particle_factor: int = np.int_):
        self._database_path = f"{find_atlas_root_dir()}/src/fluid/database.json"
        self._internal_fluxes = []
        self._surface_fluxes = []

        # TODO: VSS and VHS-VSS collision models are not implemented yet
        if collision_model not in ['ELASTIC', 'VHS', 'VSS', 'VHS-VSS']:
            raise ValueError("Collision model must be either 'ELASTIC', 'VHS', 'VSS', or 'VHS-VSS'")

        self._collision_model = collision_model
        self._macro_particle_factor = macro_particle_factor

    def get_collision_model(self) -> int:
        collision_model = ['ELASTIC', 'VHS', 'VSS', 'VHS-VSS']
        return collision_model.index(self._collision_model) + 1

    @property
    def macro_particle_factor(self):
        return self._macro_particle_factor

    @macro_particle_factor.setter
    def macro_particle_factor(self, value):
        self._macro_particle_factor = value

    @property
    def internal_fluxes(self):
        return self._internal_fluxes

    @internal_fluxes.setter
    def internal_fluxes(self, value):
        self._internal_fluxes = value

    @property
    def surface_fluxes(self):
        return self._surface_fluxes

    @surface_fluxes.setter
    def surface_fluxes(self, value):
        self._surface_fluxes = value

    @property
    def collision_model(self):
        return self._collision_model

    @collision_model.setter
    def collision_model(self, value):
        if value not in ['ELASTIC', 'VHS', 'VSS', 'VHS-VSS']:
            raise ValueError("Collision model must be either 'ELASTIC', 'VHS', 'VSS', or 'VHS-VSS'")
        self._collision_model = value

    @abc.abstractmethod
    def from_database(self, name: str):
        pass

    @abc.abstractmethod
    def to_database(self):
        pass

    @abc.abstractmethod
    def from_json(self, json: json):
        pass

    @abc.abstractmethod
    def to_json(self):
        pass

    @abc.abstractmethod
    def get_properties(self):
        pass

    def add_internal_fluxes(self,
                            space_ic: str = "cell_local",
                            velocity_distribution: str = "maxwell_lpn",
                            mw_temperature_ic: float = 300,
                            temp_vib: float = 300,
                            temp_rot: float = 300,
                            part_density: float = 1e19,
                            velo_ic: float = 0,
                            velo_vec_ic: list = None):

        if velo_vec_ic is None:
            velo_vec_ic = [1, 0, 0]
        velo_vec_ic = f'(/ {velo_vec_ic[0]}, {velo_vec_ic[1]}, {velo_vec_ic[2]} /)'

        internal_flux = {
            "SpaceIc": space_ic,
            "velocityDistribution": velocity_distribution,
            "MWTemperatureIC": mw_temperature_ic,
            "TempVib": temp_vib,
            "TempRot": temp_rot,
            "PartDensity": part_density,
            "VeloIC": velo_ic,
            "VeloVecIC": f'{velo_vec_ic}\n'
        }
        self._internal_fluxes.append(internal_flux)

    def add_surface_fluxes(self,
                           name: str or int,
                           adaptive_type: str,
                           adaptive_pressure: float,
                           velocity_distribution: str = 'maxwell_lpn',
                           mw_temperature_ic: float = 300,
                           temp_vib: float = 300,
                           temp_rot: float = 300,
                           velo_ic: float = 0,
                           velo_vec_ic: list = None,
                           adaptive: bool = True):

        if velo_vec_ic is None:
            velo_vec_ic = [1, 0, 0]
        velo_vec_ic = f'(/ {velo_vec_ic[0]} ,{velo_vec_ic[1]}, {velo_vec_ic[2]} /)'

        if adaptive_type not in ['inflow', 'outflow']:
            raise ValueError("adaptive_type must be either 'inflow' or 'outflow'")

        surface_flux = {
            "BC": name,
            "velocityDistribution": velocity_distribution,
            "MWTemperatureIC": mw_temperature_ic,
            "TempVib": temp_vib,
            "TempRot": temp_rot,
            "VeloIC": velo_ic,
            "VeloVecIC": velo_vec_ic,
            "Adaptive": adaptive,
            "Adaptive-Type": 1 if adaptive_type == 'inflow' else 2,
            "Adaptive-Pressure": adaptive_pressure
        }
        self._surface_fluxes.append(surface_flux)

    def find_max_pressure(self):
        max_pressure = 0
        boundary_names = ""

        for surface_flux in self._surface_fluxes:
            if surface_flux['Adaptive-Pressure'] > max_pressure:
                max_pressure = surface_flux['Adaptive-Pressure']
                boundary_names = surface_flux['BC']

        return max_pressure, boundary_names

    def find_min_pressure(self):
        min_pressure = 0
        boundary_names = ""

        for surface_flux in self._surface_fluxes:
            if surface_flux['Adaptive-Pressure'] < min_pressure:
                min_pressure = surface_flux['Adaptive-Pressure']
                boundary_names = surface_flux['BC']

        return min_pressure, boundary_names

    def get_temperature(self, boundary: str or int) -> float:

        if isinstance(boundary, int):
            boundary_name = self._surface_fluxes[boundary]['BC']
        else:
            boundary_name = boundary

        for surface_flux in self._surface_fluxes:
            if surface_flux['BC'] == boundary_name:
                return float(surface_flux['MWTemperatureIC'])
        raise ValueError(f"Boundary {boundary_name} not found.")
