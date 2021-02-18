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
    rev = RandomEvolution(
        orig_ind=orig_ind,
        fitness=Fitness.evaluate,
        generate=Generator.generate_random_from,
        generate_params={"min": 0, "max": 5},
        select=Selector.select_random_ev,
        timeout=40
    )
    rev.start_from()

    v_rev = Visualization(rev.logbook, expectations)
    v_rev.print_logbook()
    v_rev.visualize_evolution()

    opo_ev = OpOEvolution(
        orig_ind=orig_ind,
        fitness=Fitness.evaluate,
        generate=Generator.generate_random_from,
        generate_params={"min": 0, "max": 5},
        mutate=Mutator.mutate,
        mutate_params={"std": 0.5, "min": 0, "max": 5},
        select=Selector.select_random_ev,
        timeout=40
    )
    opo_ev.start_from()
    v_opo_ev = Visualization(opo_ev.logbook, expectations)
    v_opo_ev.print_logbook()
    v_opo_ev.visualize_evolution()
