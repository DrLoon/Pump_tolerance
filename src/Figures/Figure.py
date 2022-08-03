from typing import List, Tuple, Dict
import numpy as np
from abc import ABC


class Figure(ABC):
    def ineq(self) -> Tuple[Dict]:
        raise NotImplementedError("")

    @property
    def center(self) -> List[float]:
        raise NotImplementedError("")

    @property
    def mu_params(self) -> List[float]:
        raise NotImplementedError("")

    def add_tol_to_mu_params(self, tolerances: List[float]):
        raise NotImplementedError("")

    def all_params(self) -> List[float]:
        return self.center + self.mu_params

    def isBelongs(self, point: List[float]):
        assert len(point) == 3
        e = self.ineq()
        for i in e:
            if i['fun'](point) < 0:
                return False
        return True

    def plot(self, ax, n: int, scatter: bool = False):
        from_ = min(self.center) - max(self.mu_params)
        to_ = max(self.center) + max(self.mu_params)

        points = np.random.uniform(from_, to_, (n, 3))

        good_points = filter(self.isBelongs, points)

        if good_points == []:
            return

        p = list(zip(*good_points))
        xs, ys, zs = p
        if scatter:
            ax.scatter(xs, ys, zs)
        else:
            ax.plot(xs, ys, zs)
