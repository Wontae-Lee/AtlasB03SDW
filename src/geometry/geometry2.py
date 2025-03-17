from src.geometry.geometry import Geometry
from src.primitive.parser.hopr_ini import HoprINI


class Geometry2(Geometry):

    def __init__(self,
                 mesh_file: str,
                 axis_symmetry: bool,
                 radial_weighting: bool = False,
                 part_scale_factor: float = None,
                 clone_mode: int = 2,
                 clone_delay: int = 5,
                 surf_flux_sub_sides: int = 2):
        super().__init__(mesh_file)
        self._axis_symmetry = axis_symmetry
        self._radial_weighting = radial_weighting

        self._options = {
            "Particles-Symmetry-Order": 2,
            "Particles-Symmetry2DAxisymmetric": "T" if axis_symmetry else "F",
            "Particles-RadialWeighting": "T" if radial_weighting else "F",
        }

        self._radial_weighting_options = {
            "Particles-RadialWeighting-PartScaleFactor": part_scale_factor,
            "Particles-RadialWeighting-CloneMode": clone_mode,
            "Particles-RadialWeighting-CloneDelay": clone_delay,
            "Particles-RadialWeighting-SurfFluxSubSides": surf_flux_sub_sides
        }
        self.set_hopr_options()

        self._symmetric_z_boundaries = [
            {
                "SourceName": "LowerZ_BC",
                "Condition": "symmetric_dim",
                "BoundaryParticleOutput": "F\n"
            },
            {
                "SourceName": "UpperZ_BC",
                "Condition": "symmetric_dim",
                "BoundaryParticleOutput": "F\n"
            }
        ]
        self._symmetric_axis_boundaries = []
        self._curved_boundaries = []

    @property
    def axis_symmetry(self):
        return self._axis_symmetry

    @axis_symmetry.setter
    def axis_symmetry(self, value):
        self._axis_symmetry = value
        self._options["Particles-Symmetry2DAxisymmetric"] = "T" if value else "F"

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    @property
    def radial_weighting_options(self):
        return self._radial_weighting_options

    @radial_weighting_options.setter
    def radial_weighting_options(self, value):
        self._radial_weighting_options = value

    def set_hopr_options(self,
                         debugvisu: bool = True,
                         logging: bool = False,
                         jacobian_tolerance: float = 1e-24,
                         mode: int = 5,
                         meshscale: float = 1,
                         space_quandt: float = 1,
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

        # add options
        self._hopr_options["MeshDim"] = 2
        self._hopr_options["ZLength"] = 0.005  # \TODO: In the future, this should be set by the user
        self._hopr_options["NElemsZ"] = 1
        self._hopr_options["LowerZ_BC"] = "(/4,0,0,0/)"
        self._hopr_options["UpperZ_BC"] = "(/4,0,0,0/)"

    def create_hopr_file(self, project_name: str, hopr_file_directory: str):
        hopr_ini = HoprINI(hopr_file_directory, new_file=True)
        hopr_ini.add_text("""\
!=============================================================================== !
! OPTIONS
!=============================================================================== !
""")
        hopr_ini.add_text(f"ProjectName={project_name}")
        hopr_ini.add_text(f"FileName={self.mesh_file_name}")
        hopr_ini.add_all(self._hopr_options)
        hopr_ini.add_text("""\
!=============================================================================== !
! BOUNDARY CONDITIONS
!=============================================================================== !
""")

        for _, boundary in enumerate(self._boundary_names):
            hopr_ini.add_text(f"BoundaryName={boundary}")
            hopr_ini.add_text("BoundaryType=(/4,0,0,0/)")
        return

    def add_symmetric_axis_boundary(self, name: str, boundary_particle_output: bool = False):

        self._boundary_names.append(name)

        symmetric_axis_options = {
            "SourceName": name,
            "Condition": "symmetric_axis",
            "BoundaryParticleOutput": "T\n" if boundary_particle_output else "F\n"
        }

        self._symmetric_axis_boundaries.append(symmetric_axis_options)

    def is_axis_symmetry(self):
        return self._axis_symmetry

    def get_number_of_boundaries(self) -> int:
        num_of_boundaries = (len(self._open_boundaries)
                             + len(self._wall_boundaries)
                             + len(self._symmetric_boundaries)
                             + len(self._symmetric_axis_boundaries)
                             + len(self._curved_boundaries)
                             + len(self._symmetric_z_boundaries))
        return num_of_boundaries

    def is_radial_weighting(self):
        return self._options["Particles-RadialWeighting"]

    def get_boundary_options(self):
        options = {}
        options.update(self._options)
        if self._radial_weighting:
            options.update(self._radial_weighting_options)

        return options

    def get_all_boundaries(self):
        all_boundaries = (self._open_boundaries + self._wall_boundaries + self._symmetric_boundaries
                          + self._symmetric_axis_boundaries + self._curved_boundaries + self._symmetric_z_boundaries)
        return all_boundaries

    def get_boundary_names(self):
        boundary_names = []
        for name in self._boundary_names:
            boundary_names.append(name)
        boundary_names.append("LowerZ_BC")
        boundary_names.append("UpperZ_BC")
        return boundary_names

    def get_boundary_index(self, name: str) -> int:
        boundary_names = self.get_boundary_names()
        return boundary_names.index(name)

    def get_boundary_info(self, boundary_name: str):

        if boundary_name not in self.get_boundary_names():
            raise ValueError(f"Boundary name {boundary_name} is not in the boundary names.")

        for boundary in self.get_all_boundaries():
            if boundary["SourceName"] == boundary_name:
                return boundary

    def get_dimensions(self) -> int:
        return 2
