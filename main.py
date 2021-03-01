import numpy as np
from evolution import Selector, Generator, Fitness, Mutator
from random_evolution import RandomEvolution
from opo_evolution import OpOEvolution
from individual import Individual
from visualization import Visualization


def expectations(gens):
    # TODO: calculate maximum value for each scenario
    return [24.99 for _ in range(gens)]


if __name__ == '__main__':
    np.random.seed(64)

    orig_ind = Individual(np.random.uniform(0, 5, 1))
    epoches = 12
    rev = RandomEvolution(
        orig_ind=orig_ind,
        fitness=Fitness.evaluate,
        generate=Generator.generate_random_from,
        generate_params={"min": 0, "max": 5},
        select=Selector.select_random_ev,
        timeout=epoches
    )
    rev.run()

    opo_ev = OpOEvolution(
        orig_ind=orig_ind,
        fitness=Fitness.evaluate,
        generate=Generator.generate_random_from,
        generate_params={"min": 0, "max": 5},
        mutate=Mutator.mutate,
        mutate_params={"mean": 0, "std": 0.5, "min": 0, "max": 5},
        select=Selector.select_random_ev,
        timeout=epoches
    )
    opo_ev.run()

    v = Visualization(expectations)
    v.visualize(rev.logbook, opo_ev.logbook, "Random", "OPO")
