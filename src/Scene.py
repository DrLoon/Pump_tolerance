from Figures.Figure import Figure
from typing import List, Optional

from matplotlib import pyplot as plt

from intersection import isIntersect_pro

class Scene:
    def __init__(self, figures: Optional[List[Figure]] = None, workspace: float = 100):
        if figures is None:
            self.figures = []
        else:
            assert isinstance(figures, list) and workspace > 0
            self.figures = figures
        self.__workspace = workspace

        assert not isIntersect_pro(self.figures), "The figures intersect"

    def figures_count(self) -> int:
        return len(self.figures)

    def mutable_params_count(self) -> int:
        n = 0
        for i in self.figures:
            n += len(i.mu_params())
        return n

    def bounds_mut_params(self) -> List[List[float]]:
        r = []
        for i in self.figures:
            r += i.bounds_mut_params()
        return r

    def __is_figure_in_workspace(self, figure: Figure):
        raise NotImplementedError("")

    def plot(self, n: int = 10000, scatter: bool = False):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        for i in self.figures:
            i.plot(ax, n, scatter=scatter)
        plt.show()
