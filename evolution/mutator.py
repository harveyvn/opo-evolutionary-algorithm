import copy
import numpy


class Mutator:
    @staticmethod
    def mutate(mutate_params, deap_inds):
        mutant = copy.deepcopy(deap_inds)
        individual = mutant[0]  # deap_individual is a list
        value = individual.value
        value += numpy.random.normal(mutate_params["mean"], mutate_params["std"], 1)
        if value < mutate_params["min"]:
            value = mutate_params["min"]
        if value > mutate_params["max"]:
            value = mutate_params["max"]

        individual.value += value

        return mutant  # return deap_individual
