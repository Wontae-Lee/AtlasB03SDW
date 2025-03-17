import psutil


class Parallel:
    def __init__(self):
        self.__physical_cores = psutil.cpu_count(logical=False)
        self.__logical_cores = psutil.cpu_count(logical=True)

    @property
    def logical_cores(self):
        return self.__logical_cores

    @property
    def physical_cores(self):
        return self.__physical_cores
