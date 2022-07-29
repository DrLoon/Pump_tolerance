import numpy as np
from scipy import optimize
from tqdm import tqdm
from copy import copy
from typing import List, Tuple, Union

import pygad

from Parlgram import Parlgram
from Cylinder import Cylinder
from Sphere import Sphere
from Figure import Figure
from Scene import Scene

from intersection import isIntersect_pro
from utils import split


def add_tol_to_figures(tols: List[float], figures: List[Figure]):
    tols = split(tols, figures)
    new_figures = []
    for i in range(len(figures)):
        new_figures.append(figures[i].add_tol_to_mu_params(tols[i]))
    return new_figures

def F(x: List[float], *args: Scene) -> float:
    figures: List[Figure] = args[0].figures()

    new_figures = add_tol_to_figures(x, figures)

    if isIntersect_pro(new_figures):
        return np.random.uniform(666, 999)
    return -min(x)  # better to use "-min(x)"

def differential_evolution(scene: Scene):
    bounds = [(0, 10) for _ in range(scene.mutable_params_count())]
    sol = optimize.differential_evolution(F, args=(scene,), bounds=bounds, maxiter=100, disp=True, workers=8)
    return sol.x

def genetic_algorithm(scene: Scene):
    def fitness_func(solution, solution_idx):
        figures: List[Figure] = scene.figures()

        new_figures = add_tol_to_figures(solution, figures)

        if isIntersect_pro(new_figures):
            return -np.random.uniform(666, 999)
        return min(solution)  # better to use "-min(x)"

    def callback_on_generation(ga_instance):
        print("Generation:", ga_instance.generations_completed)
        print("Fitness of the best solution :", fitness_func(ga_instance.best_solutions[-1], 0))

    gene_space = [{'low': 0, 'high': 10} for _ in range(scene.mutable_params_count())]
    ga_instance = pygad.GA(num_generations=100,
                           num_parents_mating=5,
                           fitness_func=fitness_func,
                           num_genes=len(gene_space),
                           sol_per_pop=100,
                           gene_space=gene_space,
                           save_best_solutions=True,
                           on_generation=callback_on_generation
                           )
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    return solution

def main():
    g_parlgram = Parlgram([2, 2, 2], [2, 2, 2])
    g_parlgram2 = Parlgram([-5, -5, -5], [0.25, 0.25, 0.25])
    g_cylinder = Cylinder([0, 0, 0], 2, 1)
    g_sphere = Sphere([-15, -15, -15], 0.25)

    scene = Scene([g_parlgram, g_cylinder, g_parlgram2, g_sphere])

    solution = differential_evolution(scene)

    new_figs = add_tol_to_figures(solution, scene.figures())
    new_scene = Scene(new_figs)

    scene.plot()
    new_scene.plot()

    print("Пересекаются ли фигуры:", isIntersect_pro(new_scene.figures()))

if __name__ == '__main__':
    main()