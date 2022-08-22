from typing import List
import numpy as np

from .Figure import Figure


class Parlgram(Figure):
    def __init__(self, center: List[float], boundaries: List[float]):
        assert len(center) == 3 and len(boundaries) == 3
        assert np.all(np.greater(boundaries, 0))
        self.x0 = center[0]
        self.y0 = center[1]
        self.z0 = center[2]
        self.length = boundaries[0]
        self.width = boundaries[1]
        self.height = boundaries[2]

    @property
    def center(self) -> List[float]:
        return [self.x0, self.y0, self.z0]

    def mu_params(self) -> List[float]:
        return [self.length, self.width, self.height]

    def ineq(self):
        return (
            {'type': 'ineq', 'fun': lambda x: -1 * abs(x[0] - self.x0) + self.length / 2},  # |x-x0|<=l/2
            {'type': 'ineq', 'fun': lambda x: -1 * abs(x[1] - self.y0) + self.width / 2},  # |y-y0|<=w/2
            {'type': 'ineq', 'fun': lambda x: -1 * abs(x[2] - self.z0) + self.height / 2}  # |z-z0|<=h/2
        )

    def add_tol_to_mu_params(self, tolerances: List[float]):
        mu_params = self.mu_params()
        assert len(mu_params) == len(tolerances)
        return Parlgram(self.center,
                        [self.length + tolerances[0], self.width + tolerances[1], self.height + tolerances[2]])
