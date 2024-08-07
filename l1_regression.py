from pulp import *
import numpy as np

from matplotlib import pyplot as plt

# Given data, compute optimal parameters for a line minimizing sum of L1 errors
def l1_regression_1d(xs : np.ndarray, ys : np.ndarray):

  # empty LP
  l1_lp = LpProblem("l1_lp", LpMinimize)
  
  zs = [LpVariable(f"z{i}") for i in range(xs.size)]

  alpha = LpVariable("alpha")
  beta = LpVariable("beta")

  l1_lp += lpSum(zs)

  for zi, xi, yi in zip(zs, xs, ys):
    l1_lp += yi - alpha * xi - beta <= zi
    l1_lp += -yi + alpha * xi + beta <= zi

  l1_lp.solve()

  return (alpha.value(), beta.value(), value(l1_lp.objective))

act_alph, act_bet = 3, 5

N = 50

# increase this to observe the training error go up
std_dev = 1

xs = np.array(range(N))

# we add randomness to see that non-zero training error is possible
ys = act_alph * xs + act_bet + np.random.normal(0.0, std_dev, size=(N,))

plt.plot(xs, ys, "r+")

calc_alph, calc_bet, err = l1_regression_1d(xs, ys)
print(f"L1 error: {err}")

plt.plot(xs, calc_alph * xs + calc_bet)
plt.show()