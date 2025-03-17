from src.fluid.molecule import Molecule
from src.geometry.geometry2 import Geometry2
from src.simulator import Simulator


def create_geometry(project_name: str, project_path: str):
    import gmsh
    import sys
    import os

    # Create the project directory
    os.makedirs(project_path, exist_ok=True)

    # Initialize gmsh
    gmsh.initialize()

    # Set the mesh save option
    # This is required to run the HOPR
    gmsh.option.setNumber("Mesh.SaveAll", 1)
    gmsh.model.add(f"{project_name}")

    # set the points
    gmsh.model.geo.addPoint(0, 0, 0, tag=1)  # bottom-left
    gmsh.model.geo.addPoint(1.5, 0, 0, tag=2)  # bottom-right
    gmsh.model.geo.addPoint(1.5, .05, 0, tag=3)  # top-right
    gmsh.model.geo.addPoint(0, .05, 0, tag=4)  # top-left

    # Create lines
    gmsh.model.geo.addLine(1, 2, 1)  # bottom line
    gmsh.model.geo.addLine(2, 3, 2)  # right line
    gmsh.model.geo.addLine(3, 4, 3)  # top line
    gmsh.model.geo.addLine(4, 1, 4)  # left line

    # Create surface
    gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)
    gmsh.model.geo.addPlaneSurface([1], 1)

    # transfinite mesh
    gmsh.model.geo.mesh.setTransfiniteCurve(1, 21)
    gmsh.model.geo.mesh.setTransfiniteCurve(3, 21)
    gmsh.model.geo.mesh.setTransfiniteCurve(2, 10)
    gmsh.model.geo.mesh.setTransfiniteCurve(4, 10)
    gmsh.model.geo.mesh.setTransfiniteSurface(1, cornerTags=[1, 2, 3, 4])

    # transfinite lines
    gmsh.model.geo.mesh.setRecombine(2, 1)

    # Translate the mesh to the z-axis
    # \TODO It is currently required for HOPR to work. dz must be -0.0025!
    gmsh.model.geo.translate([(2, 1)], 0, 0, -0.0025)

    # Create physical boundaries
    gmsh.model.geo.synchronize()
    gmsh.model.addPhysicalGroup(1, [1], tag=1, name="WALL1")
    gmsh.model.addPhysicalGroup(1, [2], tag=2, name="OUT")
    gmsh.model.addPhysicalGroup(1, [3], tag=3, name="WALL2")
    gmsh.model.addPhysicalGroup(1, [4], tag=4, name="IN")

    # Generate the mesh
    gmsh.model.mesh.generate(2)

    # Save the mesh
    gmsh.write(f"{project_path}/{project_name}.msh")

    # Launch the GUI to see the results:
    # nopopup is used to avoid the GUI
    sys.argv.append("-nopopup")
    if '-nopopup' not in sys.argv:
        gmsh.fltk.run()

    gmsh.finalize()

    return f'{project_path}/{project_name}.msh'


def main():
    # Set the parameters
    project_name = "cylinder3_2d_symmetric"
    directory_path = f"simulations/{project_name}"

    # Define the fluid properties and the surface for emitting the molecules
    molecule = Molecule(collision_model="VHS", macro_particle_factor=263361931414438)
    molecule.from_database("O2")
    molecule.add_surface_fluxes(name="IN", adaptive_type="inflow", adaptive_pressure=2.5)
    molecule.add_surface_fluxes(name="OUT", adaptive_type="outflow", adaptive_pressure=1.0)

    # Create the geometry
    msh_file_path = create_geometry(project_name, project_path=f'simulations/{project_name}')
    geometry = Geometry2(mesh_file=msh_file_path, axis_symmetry=True)
    geometry.add_open_boundary(name="IN")
    geometry.add_open_boundary(name="OUT")
    geometry.add_wall_boundary(name="WALL1", wall_temp=300, trans_acc=0, vib_acc=0, rot_acc=0, momentum_acc=0.85)
    geometry.add_symmetric_axis_boundary(name="WALL2")

    # Simulation setup
    simulator = Simulator(project_name,
                          directory_path,
                          fluid=molecule,
                          geometry=geometry)

    # Run the simulation
    simulator.run(start_time=0, end_time=0.8, time_step=5e-07)

    # Rerun the simulation
    # simulator.rerun(start_time=0.8, end_time=1.6, time_step=5e-07)


if __name__ == "__main__":
    main()
