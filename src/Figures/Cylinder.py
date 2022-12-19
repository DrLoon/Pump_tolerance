from typing import List
import numpy as np

from .Figure import Figure


class Cylinder(Figure):
    def __init__(self, center: List[float], radius: float, height: float):
        assert len(center) == 3 and radius > 0 and height > 0
        self.x0 = center[0]
        self.y0 = center[1]
        self.z0 = center[2]
        self.R = radius
        self.h = height
        super().__init__()

    def _set_outer_radius(self) -> float:
        return (self.R**2 + (self.h/2)**2) ** 0.5

    @property
    def center(self) -> List[float]:
        return [self.x0, self.y0, self.z0]

    def mu_params(self) -> List[float]:
        return [self.R, self.h]

    def bounds_mut_params(self) -> List[List[float]]:
        return [[0, np.inf] for _ in self.mu_params()]

    def ineq(self):
        return (
            {'type': 'ineq', 'fun': lambda x: -1 * ((x[0] - self.x0) ** 2 + (x[1] - self.y0) ** 2) + self.R ** 2},
            # (x-x0)^2 + (y-y0)^2 <= r^2
            {'type': 'ineq', 'fun': lambda x: -1 * abs(x[2] - self.z0) + self.h / 2},  # |z-z0|<=h/2
        )

    def add_tol_to_mu_params(self, tolerances: List[float]):
        mu_params = self.mu_params()
        assert len(mu_params) == len(tolerances)
        return Cylinder(self.center, self.R + tolerances[0], self.h + tolerances[1])
