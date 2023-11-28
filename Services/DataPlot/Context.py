class Context:
    def __init__(self) -> None:
        self.strategy = None

    #new_strat é uma instância de classe que herda DataInterface
    def set_strategy(self, new_strat):
        self.strategy = new_strat

    def execute_strategy(self):
        return self.strategy.readJSON()