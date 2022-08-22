from typing import List

from .Figure import Figure


class Sphere(Figure):
    def __init__(self, center: List[float], radius: float):
        assert len(center) == 3 and radius > 0
        self.x0 = center[0]
        self.y0 = center[1]
        self.z0 = center[2]
        self.R = radius
        super().__init__()

    def _set_outer_radius(self) -> float:
        return self.R

    @property
    def center(self) -> List[float]:
        return [self.x0, self.y0, self.z0]

    def mu_params(self) -> List[float]:
        return [self.R]

    def ineq(self):
        return (
            {'type': 'ineq', 'fun':
                # (x-x0)^2 + (y-y0)^2 + (z-z0)^2 <= r^2
                lambda x: -1 * ((x[0] - self.x0) ** 2 + (x[1] - self.y0) ** 2 + (x[2] - self.z0) ** 2) + self.R ** 2},
        )

    def add_tol_to_mu_params(self, tolerances: List[float]):
        mu_params = self.mu_params()
        assert len(mu_params) == len(tolerances)
        return Sphere(self.center, self.R + tolerances[0])
