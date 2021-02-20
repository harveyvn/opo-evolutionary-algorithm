import numpy as np
from evolution import Selector, Generator, Fitness, Mutator
from random_evolution import RandomEvolution
from opo_evolution import OpOEvolution
from individual import Individual
from visualization import Visualization


def expectations(gens):
    # TODO: calculate maximum value for each scenario
    return [6.248 for _ in range(gens)]


if __name__ == '__main__':
    np.random.seed(64)

    orig_ind = Individual(np.random.uniform(0, 5, 1))
    timeout = 10
    rev = RandomEvolution(
        orig_ind=orig_ind,
        fitness=Fitness.evaluate,
        generate=Generator.generate_random_from,
        generate_params={"min": 0, "max": 5},
        select=Selector.select_random_ev,
        timeout=timeout
    )
    rev.start_from()

    opo_ev = OpOEvolution(
        orig_ind=orig_ind,
        fitness=Fitness.evaluate,
        generate=Generator.generate_random_from,
        generate_params={"min": 0, "max": 5},
        mutate=Mutator.mutate,
        mutate_params={"std": 0.5, "min": 0, "max": 5},
        select=Selector.select_random_ev,
        timeout=timeout
    )
    opo_ev.start_from()

    v = Visualization(rev.logbook, opo_ev.logbook, expectations)
    v.print_logbook(rev.logbook)
    v.print_logbook(opo_ev.logbook)
    v.visualize_evolution()
