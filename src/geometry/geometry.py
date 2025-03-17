import abc


class Geometry:

    def __init__(self, mesh_file: str):
        self.mesh_file = mesh_file
        self.mesh_file_name = mesh_file.split("/")[-1]
        self._boundary_names = []
        self._open_boundaries = []
        self._wall_boundaries = []
        self._symmetric_boundaries = []

        self._hopr_options = {
            "Debugvisu": "T",
            "Logging": "F",
            "JacobianTolerance": 1e-24,
            "Mode": 5,
            "Meshscale": 1.0,
            "SpaceQuandt": 1,
            "UseCurveds": "F",
            "rebuildCurveds": "F",
        }

    def set_hopr_options(self,
                         debugvisu: bool = True,
                         logging: bool = False,
                         jacobian_tolerance: float = 1e-24,
                         mode: int = 5,
                         meshscale: float = 1.0,
                         space_quandt: int = 1,
                         use_curveds: bool = False,
                         rebuild_curveds: bool = False):
        self._hopr_options["Debugvisu"] = "T" if debugvisu else "F"
        self._hopr_options["Logging"] = "T" if logging else "F"
        self._hopr_options["JacobianTolerance"] = jacobian_tolerance
        self._hopr_options["Mode"] = mode
        self._hopr_options["Meshscale"] = meshscale
        self._hopr_options["SpaceQuandt"] = space_quandt
        self._hopr_options["UseCurveds"] = "T" if use_curveds else "F"
        self._hopr_options["rebuildCurveds"] = "T" if rebuild_curveds else "F"

    def add_open_boundary(self, name: str, boundary_particle_output: bool = False):
        self._boundary_names.append(name)

        open_boundary_options = {
            "SourceName": name,
            "Condition": "open",
            "BoundaryParticleOutput": "T\n" if boundary_particle_output else "F\n"
        }
        self._open_boundaries.append(open_boundary_options)

    def add_wall_boundary(self,
                          name: str,
                          wall_temp: float = 300,
                          momentum_acc: float = 1,
                          trans_acc: float = 1,
                          vib_acc: float = 1,
                          rot_acc: float = 1,
                          boundary_particle_output: bool = False):
        self._boundary_names.append(name)

        wall_boundary_options = {
            "SourceName": name,
            "Condition": "reflective",
            "WallTemp": wall_temp,
            "MomentumACC": momentum_acc,
            "TransACC": trans_acc,
            "VibACC": vib_acc,
            "RotACC": rot_acc,
            "BoundaryParticleOutput": "T\n" if boundary_particle_output else "F\n"
        }

        self._wall_boundaries.append(wall_boundary_options)

    def add_symmetric_boundary(self, name: str, boundary_particle_output: bool = False):
        self._boundary_names.append(name)

        symmetric_boundary_options = {
            "SourceName": name,
            "Condition": "symmetric_dim",
            "BoundaryParticleOutput": "T\n" if boundary_particle_output else "F\n"
        }
        self._symmetric_boundaries.append(symmetric_boundary_options)

    def get_boundary_index(self, name: str) -> int:
        return self._boundary_names.index(name)

    @abc.abstractmethod
    def get_dimensions(self) -> int:
        pass

    @abc.abstractmethod
    def create_hopr_file(self, project_name: str, hopr_file_directory: str):
        pass

    @abc.abstractmethod
    def is_axis_symmetry(self):
        pass

    @abc.abstractmethod
    def get_number_of_boundaries(self) -> int:
        pass

    @abc.abstractmethod
    def is_radial_weighting(self):
        pass

    @abc.abstractmethod
    def get_all_boundaries(self):
        pass

    @abc.abstractmethod
    def get_boundary_options(self):
        pass

    @abc.abstractmethod
    def get_boundary_names(self):
        pass

    @abc.abstractmethod
    def get_boundary_info(self, boundary_name: str):
        pass
