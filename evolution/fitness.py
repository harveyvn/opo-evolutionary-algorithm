class Fitness:
    @staticmethod
    def evaluate(deap_inds):
        individual = deap_inds[0]
        try:
            x = individual.value[0]
            return -x*(x-1)*(x-2)*(x-3)*(x-4),
        except Exception as inst:
            print(type(inst), inst, deap_inds[0])  # the exception instance
            return 0,
