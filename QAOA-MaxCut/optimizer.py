from abc import ABC, abstractmethod
from scipy.optimize import minimize

class Optimizer(ABC):
    @abstractmethod
    def optimize(self, objective, initial_params):
        pass

class ScipyOptimizer(Optimizer):

    def __init__(self, method="COBYLA", maxiter=200):
        self.method = method
        self.maxiter = maxiter

    def optimize(self, objective, initial_params):
        return minimize(
            objective,
            initial_params,
            method=self.method,
            options={"maxiter": self.maxiter}
        )