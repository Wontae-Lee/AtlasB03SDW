import os

import numpy as np


def random_parameters(min_value: float,
                      max_value: float,
                      n: int):
    return np.random.uniform(min_value, max_value, n)


def linear_parameters(start: float,
                      end: float,
                      n: int):
    return np.linspace(start, end, n)


def same_parameters(value: float,
                    n: int):
    return np.full(n, value)


def save_history(directory_path: str, index: int, history: str = 'history', STATE: bool = False):
    # Create directory if it does not exist
    history_directory = f'{directory_path}/{history}{str(index)}'
    os.makedirs(history_directory, exist_ok=True)

    for file in os.listdir(directory_path):
        if file.endswith('.h5') and '_DSMCState_' in file:
            # move the file to the history directory
            os.rename(f'{directory_path}/{file}', f'{history_directory}/{file}')
        elif file.endswith('.h5') and '_mesh' in file:
            # copy the file to the history directory
            os.system(f'cp {directory_path}/{file} {history_directory}/{file}')
        elif file.endswith('.h5') and STATE and '_State_' in file:
            # copy the file to the history directory
            os.system(f'cp {directory_path}/{file} {history_directory}/{file}')
        elif (file.endswith('.ini') or file.endswith('.geo') or file.endswith('.msh') or file.endswith('.log') or
              file.endswith('.sh') or file.endswith('.csv') or file.endswith('.dat') or file.endswith('.vtu')):
            # copy the file to the history directory
            os.system(f'cp {directory_path}/{file} {history_directory}/{file}')


def clean_up(directory_path: str):
    # Remove the files in the directory
    for file in os.listdir(directory_path):
        if file.endswith('.h5'):
            # if it is mesh file then skip
            if '_mesh' in file:
                continue

            os.remove(f'{directory_path}/{file}')
