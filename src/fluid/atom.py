import json

import numpy as np

from src.fluid.fluid import Fluid


class Atom(Fluid):

    def __init__(self,
                 collision_model: str,
                 name: str = None,
                 mass_ic: float = None,
                 Tref: float = None,
                 dref: float = None,
                 omega: float = None,
                 heat_of_formation: float = None,
                 macro_particle_factor: int = np.int_):
        super().__init__(collision_model, macro_particle_factor)

        self._properties = {
            'Name': name,
            'InteractionID': 1,
            'MassIc': mass_ic,
            'Tref': Tref,
            'dref': dref,
            'omega': omega,
            'HeatOfFormation_K': heat_of_formation,
        }

    def get_properties(self):
        return self._properties

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, value):
        self._properties = value

    def from_database(self, name: str):
        # Check if molecule is in database
        database = json.loads(open(f"{self._database_path}").read())
        molecules = database["InteractionID_1"]
        molecule = [data for data in molecules if data["Name"] == name][0]

        self._properties["Name"] = molecule["Name"]
        self._properties["MassIc"] = molecule["MassIc"]
        self._properties["Tref"] = molecule["Tref"]
        self._properties["dref"] = molecule["dref"]
        self._properties["omega"] = molecule["omega"]
        self._properties["HeatOfFormation_K"] = molecule["HeatOfFormation_K"]

    def to_database(self):
        pass

    def from_json(self, json: json):
        pass

    def to_json(self):
        pass
