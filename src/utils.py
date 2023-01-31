from typing import List
import numpy as np

from Figures.Figure import Figure

def split(x: List[float], figures: List[Figure]) -> List[List[float]]:
    res = []
    prev_n = 0
    for i in figures:
        n = len(i.mu_params())
        res.append(x[prev_n: prev_n + n])
        prev_n += n
    return res

def distance(x: List[float], y: List[float]) -> float:
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2) ** 0.5

def add_tol_to_figures(tols: List[float], figures: List[Figure]):
    tols = split(tols, figures)
    new_figures = []
    for i in range(len(figures)):
        new_figures.append(figures[i].add_tol_to_mu_params(tols[i]))
    return new_figures

def convert_from_norm(x: List[float], bounds: List[List[float]]):
    res = []
    for i in range(len(x)):
        assert 0 <= x[i] <= 1
        assert bounds[i][0] == 0 and bounds[i][1] >= 0
        if bounds[i][1] == np.inf:
            res.append(1.0 / (1 - x[i]) - 1.0)
        else:
            res.append(x[i] * bounds[i][1])

    return res