import numpy as np
from scipy import optimize
from typing import List

from itertools import combinations

from Figures.Figure import Figure
from utils import distance


def pre_outer_raidus_diff(figure_1: Figure, figure_2: Figure) -> float:
    s = distance(figure_1.center, figure_2.center)
    return s - (figure_1.outer_radius + figure_2.outer_radius)


def isIntersect_pro_pair(figure_1: Figure, figure_2: Figure) -> bool:
    r_diff = pre_outer_raidus_diff(figure_1, figure_2)
    if r_diff > 0:
        return False

    cons = figure_1.ineq() + figure_2.ineq()
    f = lambda x: 0
    # method= COBYLA, SLSQP
    # noinspection PyTypeChecker
    sol = optimize.minimize(f, x0=np.random.uniform(-1, 1, 3), constraints=cons, method="COBYLA")
    return sol.success


def isIntersect_pro(figures: List[Figure]) -> bool:
    combs = combinations(figures, 2)
    for i in combs:
        if isIntersect_pro_pair(i[0], i[1]):
            return True
    return False


def isIntersect_pro_1_to_many(figure: Figure, figures: List[Figure]) -> bool:
    for i in figures:
        if isIntersect_pro_pair(figure, i):
            return True
    return False
