"""
This file manages Deterministic-optimizing libaries for the D3ploy cyclus modules.

"""
import numpy as np
import statsmodels.tsa.holtwinters as hw


def polyfit_regression(ts, back_steps=10, degree=1):
    """
    Fits a polynomial to the entries in timeseries [ts]
    to predict the next value.

    Parameters:
    -----------
    ts: Array of floats
        An array of times series data to be used for the polyfit regression
    backsteps: int
        Number of backsteps to fit. (default=all past data)
    degree: int
        Degree of the fitting polynomial
    Returns:
    --------
    x : The predicted value from the fit polynomial.
    """
    time = range(1, len(ts) + 1)
    timeseries = np.array(list(ts.values()))
    fit = np.polyfit(time[-back_steps:],
                     timeseries[-back_steps:], deg=degree)
    eq = np.poly1d(fit)
    x = eq(len(ts) + 1)
    return x


def exp_smoothing(ts, back_steps=10, degree=1):
    """
    Predicts next value using simple exponential smoothing.
    Parameters:
    -----------
    ts: Array of floats
        An array of times series data to be used for the polyfit regression
    Returns:
    --------
    x : The predicted value from the exponential smoothing method.

    """
    timeseries = np.array(list(ts.values()))
    timeseries = timeseries[-back_steps:]
    if len(timeseries) == 1:
        timeseries = np.append(timeseries, timeseries[-1])
    # exponential smoothing errors when there are five datapoints
    # average is appended to the beginning of the timeseries for minimal impact
    # https://github.com/statsmodels/statsmodels/issues/4878
    elif len(timeseries) == 5:
        timeseries = np.append(np.mean(timeseries), timeseries)

    model = hw.SimpleExpSmoothing(timeseries)
    model_fit = model.fit()
    x = model_fit.predict(len(timeseries), len(timeseries))
    return x[0]

def holt_winters(ts, back_steps=10, degree=1):
    """
    Predicts next value using triple exponential smoothing
    (holt-winters method). 
    Parameters:
    -----------
    ts: Array of floats
        An array of times series data to be used for the polyfit regression
    Returns:
    --------
    x : The predicted value from the holt-winters method.
    """
    timeseries = np.array(list(ts.values()))
    timeseries = timeseries[-back_steps:]
    # exponential smoothing errors when there is only one datapoint
    if len(timeseries) == 1:
        timeseries = np.append(timeseries, timeseries[-1])
    # exponential smoothing errors when there are five datapoints
    # average is appended to the beginning of the timeseries for minimal impact
    # https://github.com/statsmodels/statsmodels/issues/4878
    elif len(timeseries) == 5:
        timeseries = np.append(np.mean(timeseries), timeseries)
    model = hw.ExponentialSmoothing(timeseries)
    model_fit = model.fit()
    x = model_fit.predict(len(timeseries), len(timeseries))
    return x[0]
