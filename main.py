import time

import numpy as np
from evolution import Selector, Generator, Fitness
from random_evolution import RandomEvolution
from individual import Individual


def expectations(gens):
    # TODO: calculate maximum value for each scenario
    return [6.248 for _ in range(gens)]


if __name__ == '__main__':
    np.random.seed(64)
    orig_ind = Individual(np.random.uniform(0, 5, 1))
    rev = RandomEvolution(
        orig_ind=orig_ind,
        fitness=Fitness.evaluate,
        generate=Generator.generate_random_from,
        generate_params={"min": 0, "max": 5},
        select=Selector.select_random_ev,
        expectations=expectations,
        timeout=30
    )
    rev.start_from()

    rev.print_logbook()
    rev.visualize_evolution()
