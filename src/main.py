import numpy as np
from scipy import optimize
from tqdm import tqdm
from copy import copy
from typing import List, Tuple, Union

from Parlgram import Parlgram
from Cylinder import Cylinder
from Sphere import Sphere
from Figure import Figure

from matplotlib import pyplot as plt

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


def isIntersect_pro(cyl: Figure, parl: Figure) -> bool:
    cons = parl.ineq() + cyl.ineq()

    f = lambda x: 0
    # method= COBYLA, SLSQP
    sol = optimize.minimize(f, x0=np.random.uniform(-1, 1, 3), constraints=cons, method="COBYLA")
    return sol.success

def F(x: List[float], *args: Figure) -> float:
    const_parlgram, const_cylinder = args

    new_cyl = const_cylinder.add_tol_to_mu_params(x[:len(const_cylinder.mu_params)])
    new_parl = const_parlgram.add_tol_to_mu_params(x[len(const_cylinder.mu_params):])

    if isIntersect_pro(cyl=new_cyl, parl=new_parl):
        return 666
    return -min(x)*100 - sum(x)  # better to use "-min(x)"


if __name__ == '__main__':
    g_parlgram = Parlgram([2, 2, 2], [2, 2, 2])
    g_cylinder = Cylinder([0, 0, 0], 2, 1)
    g_sphere = Sphere([-5, -5, -5], 0.25)

    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # g_parlgram.plot(ax, 10000, scatter=True)
    # g_cylinder.plot(ax, 10000, scatter=True)
    # g_sphere.plot(ax, 1000, scatter=True)
    # plt.show()

    bounds = [(0, 1) for _ in range(5)]
    sol = optimize.differential_evolution(F, args=(g_parlgram, g_cylinder), bounds=bounds, maxiter=100, disp=True, workers=8)
    print(sol)


    print(isIntersect_pro(g_cylinder, g_parlgram))