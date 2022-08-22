import numpy as np
from scipy import optimize
from typing import List

from itertools import combinations

from Figures.Parlgram import Parlgram
from Figures.Cylinder import Cylinder
from Figures.Figure import Figure


# deprecated
def isIntersect(cyl: Cylinder, parl: Parlgram):
    def f(x, *args):
        return [
            # Parlgram
            abs(x[0] - parl.x0) - parl.length / 2,
            abs(x[1] - parl.y0) - parl.width / 2,
            abs(x[2] - parl.z0) - parl.height / 2,

            # Cylinder
            (x[0] - cyl.x0) ** 2 + (x[1] - cyl.y0) ** 2 - cyl.R ** 2,
            abs(x[2] - cyl.z0) - cyl.h / 2
        ]

    sol = optimize.root(f, x0=np.ones(5))
    print(sol)
    print(f(sol.x)[:3])

    return sol.x


def isIntersect_pro_pair(figure_1: Figure, figure_2: Figure) -> bool:
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
