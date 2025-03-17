from src.geometry.geometry import Geometry


class Geometry3(Geometry):

    def __init__(self, mesh_file: str):
        super().__init__(mesh_file)

    def create_hopr_file(self, project_name: str, hopr_file_directory: str):
        pass

    def is_axis_symmetry(self):
        return False
