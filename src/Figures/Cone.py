from typing import List
import numpy as np

from .Figure import Figure


class Cone(Figure):
    def __init__(self, center: List[float], angle: float, height: float, upper_cut: float = 0):
        assert len(center) == 3
        assert 0 < angle <= np.pi / 2 and height > 0
        assert 0 <= upper_cut < height
        self.x0 = center[0]
        self.y0 = center[1]
        self.z0 = center[2]
        self.angle = angle
        self.height = height
        self.upper_cut = upper_cut
        super().__init__()

    def _set_outer_radius(self) -> float:
        return max(self.height * 2, self.height * np.tan(self.angle))

    @property
    def center(self) -> List[float]:
        return [self.x0, self.y0, self.z0]

    def mu_params(self) -> List[float]:
        if self.upper_cut:
            return [self.angle, self.height, self.upper_cut]
        else:
            return [self.angle, self.height]

    def bounds_mut_params(self) -> List[List[float]]:
        if self.upper_cut:
            return [[0, np.pi/2 - self.angle], [0, np.inf], [0, self.upper_cut]]
        else:
            return [[0, np.pi/2 - self.angle], [0, np.inf]]

    def ineq(self):
        def f(x):
            xx = [x[0] - self.x0, x[1] - self.y0, x[2] - self.z0]
            return -(xx[0]*xx[0] + xx[1]*xx[1]) * (1/np.tan(self.angle))**2 + xx[2] * xx[2]
        return (
            # sqrt(x^2 + y^2)*ctg(t)*sign(ctg(t))
            {'type': 'ineq', 'fun': lambda x: f(x)},
            {'type': 'ineq', 'fun': lambda x: -1 * x[2] + self.z0 - self.upper_cut},  # z < z0
            {'type': 'ineq', 'fun': lambda x: x[2] - (self.z0 - self.height)},  # z > z0 - h
        )

    def add_tol_to_mu_params(self, tolerances: List[float]):
        mu_params = self.mu_params()
        assert len(mu_params) == len(tolerances)
        assert self.angle + tolerances[0] <= np.pi / 2, 'It was ' + str(self.angle) + ' and added' + str(tolerances[0])
        if self.upper_cut:
            assert 0 <= self.upper_cut - tolerances[2] <= self.upper_cut
            return Cone(self.center, self.angle + tolerances[0], self.height + tolerances[1], self.upper_cut - tolerances[2])
        else:
            return Cone(self.center, self.angle + tolerances[0], self.height + tolerances[1])

