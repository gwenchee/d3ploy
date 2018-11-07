"""
This file manages Non-optimizing libaries for the D3ploy cyclus modules.
This supports Autoregressiving Moving Average (ARMA) and Autoregressive
Conditional Heteroskedasticisty.  
"""
import numpy as np

import statsmodels.api as sm
from arch import arch_model

def moving_avg(ts, steps=1, std_dev = 0, back_steps=5):
    """
    Calculates the moving average of a previous [order] entries in
    timeseries [ts]. It will automatically reduce the order if the
    length of ts is shorter than the order.
    Parameters:
    -----------
    ts : Array of doubles
        An array of time series data to be used for the arma prediction
    order : int
        The number of values used for the moving average.
    Returns
    -------
    x : The moving average calculated by the function.
    """
    supply = np.array(list(ts.values()))
    if steps >= len(supply):
        steps = len(supply) * -1
    else:
        steps *= -1
    x = np.average(supply[steps:])
    return x

def predict_arma(ts, steps=2, std_dev = 0, back_steps=5):
    """
    Predict the value of supply or demand at a given time step using the
    currently available time series data. This method impliments an ARMA
    calculation to perform the prediciton.
    Parameters:
    -----------
    ts : Array of doubles
        An array of time series data to be used for the arma prediction
    time: int
        The number of timesteps to predict forward.
    Returns:
    --------
    x : Predicted value for the time series at chosen timestep (time).
    """
    v = list(ts.values())
    v = v[-1*back_steps:]
    fit = sm.tsa.ARMA(v, (1,0)).fit(disp=-1)
    forecast = fit.forecast(steps)
    x = forecast[0][steps-1] + forecast[1][steps-1]*std_dev
    return x

def predict_arch(ts, steps=2, std_dev = 0, back_steps=10):
    """
    Predict the value of supply or demand at a given time step using the
    currently available time series data. This method impliments an ARCH
    calculation to perform the prediciton.
    """
    v = list(ts.values())
    model = arch_model(v)
    fit = model.fit(disp='nothing', update_freq=0, show_warning=False)
    forecast = fit.forecast(horizon=steps)
    step = 'h.' + str(steps)
    x = forecast.mean.get(step)[len(v)-steps]
    sd = math.sqrt(forecast.variance.get(step)[len(v)-steps]) * std_dev
    return x+sd
