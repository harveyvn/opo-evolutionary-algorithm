import time
import numpy as np
from deap import tools, creator, base

FIRST = 0


class OpOEvolution:
    def __init__(self, orig_ind, fitness, generate, generate_params, select, mutate, mutate_params, timeout=None):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        # Attribute generator
        self.toolbox.register("random_ind", generate, orig_ind, generate_params)
        # Structure initializers
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.random_ind, 1)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("mutate", mutate, mutate_params)
        self.toolbox.register("evaluate", fitness)
        self.toolbox.register("select", select)

        stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats_size = tools.Statistics(key=len)
        self.mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
        self.mstats.register("avg", np.mean)
        self.mstats.register("std", np.std)
        self.mstats.register("min", np.min)
        self.mstats.register("max", np.max)
        self.logbook = tools.Logbook()

        self.timeout = timeout
        self.orig_ind = orig_ind

    def run(self):
        pop = self.toolbox.population(n=1)
        pop[FIRST][FIRST] = self.orig_ind
        # Evaluate the entire population
        print("Start evaluation")
        start_time = time.time()
        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        print("Evaluation time: ", time.time() - start_time)

        best_ind = tools.selBest(pop, 1)[FIRST]
        # Begin the evolution
        print("Start of evolution")

        epochs = 0
        while epochs < self.timeout:
            epochs = epochs + 1
            # A new generation
            mutant = self.toolbox.mutate(best_ind)
            pop[:] = [mutant]
            # Evaluate the entire population
            print("Compare 2 scenarios: ")
            s1 = best_ind[0]
            s2 = pop[0][0]
            print("Best ind: ", s1)
            print("Mutant: ", s2)

            fitnesses = list(map(self.toolbox.evaluate, pop))
            for ind, fit in zip(pop, fitnesses):
                ind.fitness.values = fit

            # Select the next generation individuals
            print("Compare 2 fitness score scenarios: ")
            print("Best ind: ", best_ind.fitness.values)
            print("Mutant: ", pop[0].fitness.values)

            best_ind = self.toolbox.select(best_ind, pop)
            pop[:] = [best_ind]
            record = self.mstats.compile(pop)
            self.logbook.record(gen=epochs, evals=epochs, **record)
            print("-------------------")

