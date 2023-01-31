import numpy as np
from scipy import optimize
from tqdm import tqdm
from copy import copy
from typing import List, Tuple, Union

from Figures.Figure import Figure
from Figures.Parlgram import Parlgram
from Figures.Cylinder import Cylinder
from Figures.Sphere import Sphere
from Figures.Cone import Cone
from Scene import Scene

from intersection import isIntersect_pro
from utils import add_tol_to_figures, convert_from_norm


def F(x: List[float], *args: Scene) -> float:
    figures: List[Figure] = args[0].figures
    bounds = np.clip(args[0].bounds_mut_params(), 0, 10)
    real = convert_from_norm(x, bounds)
    new_figures = add_tol_to_figures(real, figures)

    if inter := isIntersect_pro(new_figures):
        return inter

    return -min(x)-sum(x)

def differential_evolution(scene: Scene):
    bounds = [[0,1] for _ in range(scene.mutable_params_count())]
    sol = optimize.differential_evolution(F, args=(scene,), bounds=bounds, maxiter=200, disp=True, workers=8, polish=False)
    bounds = np.clip(scene.bounds_mut_params(), 0, 10)
    print(sol.x)
    real = convert_from_norm(sol.x, bounds)
    return real

def main():
    g_parlgram = Parlgram([2, 2, 2], [2, 2, 2])
    g_parlgram2 = Parlgram([-5, -5, -5], [0.25, 0.25, 0.25])
    g_cylinder = Cylinder([0, 0, 0], 2, 1)
    g_sphere = Sphere([-15, -15, -15], 0.25)

    cone = Cone([9,9,9], 3.1415/8, 5, 3)
    # scene = Scene([cone])
    # scene.plot(n=1000000, scatter=True)

    scene = Scene([g_parlgram, g_cylinder, g_parlgram2, g_sphere, cone, Cylinder([14,11,5], 2, 1)])
    solution = differential_evolution(scene)
    print(solution)

    new_figs = add_tol_to_figures(solution, scene.figures)
    new_scene = Scene(new_figs)

    scene.plot()
    new_scene.plot(n=100000)

    print("Пересекаются ли фигуры:", isIntersect_pro(new_scene.figures))

if __name__ == '__main__':
    main()
