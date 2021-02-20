import copy
import numpy as np


class Generator:
    @staticmethod
    def generate_random_from(individual, generate_params):
        np.random.seed(64)
        random_ind = copy.deepcopy(individual)
        random_ind.value = np.random.uniform(generate_params["min"], generate_params["max"], 1)
        return random_ind
