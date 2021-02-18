class Individual():
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)