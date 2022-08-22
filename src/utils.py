from typing import List

from Figures.Figure import Figure

def split(x: List[float], figures: List[Figure]) -> List[List[float]]:
    res = []
    prev_n = 0
    for i in figures:
        n = len(i.mu_params())
        res.append(x[prev_n: prev_n + n])
        prev_n = n
    return res

def distance(x: List[float], y: List[float]) -> float:
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2])) ** 0.5
