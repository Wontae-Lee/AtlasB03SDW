import os

import psutil


def generate_scripts(directory_path: str, parallel: int = None):
    os.makedirs(directory_path, exist_ok=True)
    if parallel is None:
        parallel = psutil.cpu_count(logical=False)

    with open(f'{directory_path}/allrun.sh', 'w') as f:
        f.write(f"""\
$hopr hopr.ini
mpirun -np {parallel} $piclas parameter.ini
""")

    with open(f'{directory_path}/clean.sh', 'w') as f:
        f.write("""\
#!/bin/bash

# specific directory
directory="./"

# Loop through all files in the directory.
for filename in "$directory"/*; do
    
    # file exists, not a symbolic link, and not a directory.
    if [ -f "$filename" ] && [ ! -L "$filename" ] && [ ! -d "$filename" ]; then
        # Extract the extension from the filename.
        extension="${filename##*.}"

        # If the extension is h5, vtu, out, dat, csv, msh, or tmp, remove the file.
        if [ "$extension" = "h5" ] || [ "$extension" = "vtu" ]|| [ "$extension" = "out" ] || [ "$extension" = "dat" ] ||
        [ "$extension" = "csv" ] || [ "$extension" = "tmp" ] || [ "$extension" = "104" ] ||
        [ "$extension" = "lock" ]; 
            then
            # Remove the file.
            rm -rf "$filename"
        fi
    fi
done

""")

    with open(f'{directory_path}/run.sh', 'w') as f:
        f.write(f"""\
mpirun -np {parallel} $piclas parameter.ini
""")

    with open(f'{directory_path}/piclas2vtk.sh', 'w') as f:
        f.write("""\
#!/bin/bash

# If you want to verify a particular directory, enter its path.
directory="./"

# Run a loop for all files within the directory.
for filename in "$directory"/*; do
    # Process only if the file exists, the file is not a symbolic link, and the file is not a directory.
    if [ -f "$filename" ] && [ ! -L "$filename" ] && [ ! -d "$filename" ]; then
        # Extract the extension from the filename.
        extension="${filename##*.}"

        # If the extension is h5, run the piclas2vtk program.
        if [ "$extension" = "h5" ]; then
            # Run the piclas2vtk program.
            $piclas2vtk parameter.ini "$filename"
        fi
    fi
done
""")


def generate_run_all(case_name: str or list,
                     start_case: int,
                     end_case: int,
                     simulation_directory_path: str = "./simulations",
                     shut_down: bool = False):
    if type(case_name) is str:
        case_name = [case_name]
    allrun = f"""
cd {simulation_directory_path}
"""
    for name in case_name:

        for i in range(start_case, end_case):
            allrun += f"cd {name}{i}\n"
            allrun += "sh allrun.sh\n"
            allrun += "cd ..\n"
    if shut_down:
        allrun += "shutdown -h now\n"

    with open(f"./run_all.sh", "w") as file:
        file.write(allrun)


def generate_clean_all(case_name: str or list, start_case: int, end_case: int,
                       simulation_directory_path: str = "./simulations"):
    if type(case_name) is str:
        case_name = [case_name]
    allclean = f"""
cd {simulation_directory_path}
"""
    for name in case_name:

        for i in range(start_case, end_case):
            allclean += f"cd {name}{i}\n"
            allclean += "sh clean.sh\n"
            allclean += "cd ..\n"
        with open(f"./clean_all.sh", "w") as file:
            file.write(allclean)


def generate_visualize_all(case_name: str or list, start_case: int, end_case: int,
                           simulation_directory_path: str = "./simulations"):
    if type(case_name) is str:
        case_name = [case_name]
    allclean = f"""
cd {simulation_directory_path}
"""
    for name in case_name:
        for i in range(start_case, end_case):
            allclean += f"cd {name}{i}\n"
            allclean += "sh piclas2vtk.sh\n"
            allclean += "cd ..\n"
        with open(f"./visualize_all.sh", "w") as file:
            file.write(allclean)
