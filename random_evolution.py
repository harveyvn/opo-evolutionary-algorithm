import time
import numpy as np
import matplotlib.pyplot as plt
from deap import tools, creator, base
from threading import Thread, Event

# Event object used to send signals from one thread to another
STOP_EVENT = Event()
FIRST = 0

class RandomEvolution:
    def __init__(self, orig_ind, fitness, generate, generate_params, select, expectations, timeout=None):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        # Attribute generator
        self.toolbox.register("random_ind", generate, orig_ind, generate_params)
        # Structure initializers
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.random_ind, 1)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

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

        self.expectations = expectations
        self.timeout = timeout

    def start_from(self):
        pop = self.toolbox.population(n=1)
        # Evaluate the entire population
        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        best_ind = tools.selBest(pop, 1)[FIRST]
        epochs = 0
        # Begin the evolution
        print("Start of evolution")

        # timeout = time.time() + 10 if self.timeout is None else time.time() + self.timeout
        # while time.time() < timeout:
        epochs = 0
        while epochs < self.timeout:
            epochs = epochs + 1
            # A new generation
            pop = self.toolbox.population(n=1)
            # Evaluate the entire population
            fitnesses = list(map(self.toolbox.evaluate, pop))
            for ind, fit in zip(pop, fitnesses):
                ind.fitness.values = fit

            # Select the next generation individuals
            best_ind = self.toolbox.select(best_ind, pop)
            pop[:] = [best_ind]
            record = self.mstats.compile(pop)
            self.logbook.record(gen=epochs, evals=epochs, **record)


    def print_logbook(self):
        self.logbook.header = "gen", "evals", "fitness", "size"
        self.logbook.chapters["fitness"].header = "min", "avg", "max"
        print(self.logbook)

    def visualize_evolution(self):
        gen = self.logbook.select("gen")
        fit_maxs = self.logbook.chapters["fitness"].select("max")

        fig, ax1 = plt.subplots()
        line1 = ax1.plot(gen, fit_maxs, "b-", label="Fitness")
        line3 = ax1.plot(gen, self.expectations(len(gen)), "r-", label="Expectation")
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Fitness", color="b")
        ax1.set_xticks(gen)
        for tl in ax1.get_yticklabels():
            tl.set_color("b")

        lns = line1 + line3
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc="lower right")

        plt.show()
