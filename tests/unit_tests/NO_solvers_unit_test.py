# This file contains unit tests for functions in d3ploy/NO_solvers.py

import d3ploy.NO_solvers as no
import numpy as np 
from random import randint as rand

def test_predict_arma(): 
    """ Tests if arma is working correctly 
    """

    dict = {}
    backsteps = rand(1,5)
    number_of_timesteps = rand(6,100)
    for x in range(0,number_of_timesteps): 
        dict[x+1] = rand(0,100) 

    y = no.predict_ma(dict,backsteps)
    dict_values = np.array(list(dict.values()))
    diff = number_of_timesteps - backsteps 
    exact_y = np.average(dict_values[diff:len(dict_values)])
    assert(y == exact_y)

