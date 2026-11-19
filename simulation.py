# -*- coding: utf-8 -*-
"""
simulation.py
Monte Carlo simulation of one year of losses for a single risk.

@author: dom
"""

import numpy as np

# spread of breach costs, fitted to the HHS provider hacking sizes (assumption)
SIGMA = 2.25


def simulate_year(risk):
    # how many incidents happen this year (usually 0)
    count = np.random.poisson(risk.incidents)
    total = 0
    for i in range(count):
        # cost of one incident: median is risk.cost, with a heavy right tail
        cost = np.random.lognormal(np.log(risk.cost), SIGMA)
        total = total + cost
    return total
