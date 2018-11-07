import json
import re
import subprocess
import os
import sqlite3 as lite
import pytest
import copy
import glob
import sys
from matplotlib import pyplot as plt
import numpy as np
import operator 

def get_cursor(file_name):
    """ Connects and returns a cursor to an sqlite output file

    Parameters
    ----------
    file_name: str
        name of the sqlite file

    Returns
    -------
    sqlite cursor3
    """
    con = lite.connect(file_name)
    con.row_factory = lite.Row
    return con.cursor()

def supply_demand_dict_driving(sqlite,demand,commod):
    cur = get_cursor(sqlite)
    tables = {}
    tables[0] = "timeseriessupply"+commod
    tables[1] = "timeseries"+commod+"calc_demand"
    tables[2] = "timeseries"+commod+"calc_supply"
    fuel_supply = cur.execute("select time, sum(value) from "+tables[0]+" group by time").fetchall()
    calc_fuel_demand = cur.execute("select time, sum(value) from "+tables[1]+" group by time").fetchall()
    calc_fuel_supply = cur.execute("select time, sum(value) from "+tables[2]+" group by time").fetchall()
    dict_demand = {}
    dict_supply = {}
    dict_calc_demand = {}
    dict_calc_supply = {}
    for x in range(0,len(fuel_supply)):
        dict_supply[fuel_supply[x][0]] = fuel_supply[x][1]
        dict_calc_demand[fuel_supply[x][0]+1] = calc_fuel_demand[x][1]
        dict_calc_supply[fuel_supply[x][0]+1] = calc_fuel_supply[x][1]
    t = np.fromiter(dict_supply.keys(),dtype=float)
    fuel_demand = eval(demand)
    if isinstance(fuel_demand,int):
        fuel_demand = fuel_demand*np.ones(len(t))
    for x in range(0,len(fuel_supply)):
        dict_demand[fuel_supply[x][0]] = fuel_demand[x]

    return dict_demand, dict_supply, dict_calc_demand, dict_calc_supply


def supply_demand_dict_nondriving(sqlite,commod):
    cur = get_cursor(sqlite)
    tables = {}
    tables[0] = "timeseriessupply"+commod
    tables[1] = "timeseries"+commod+"calc_demand"
    tables[2] = "timeseries"+commod+"calc_supply"
    tables[3] = "timeseriesdemand"+commod
    fuel_demand = cur.execute("select time, sum(value) from "+tables[3]+" group by time").fetchall()
    fuel_supply = cur.execute("select time, sum(value) from "+tables[0]+" group by time").fetchall()
    calc_fuel_demand = cur.execute("select time, sum(value) from "+tables[1]+" group by time").fetchall()
    calc_fuel_supply = cur.execute("select time, sum(value) from "+tables[2]+" group by time").fetchall()
    dict_demand = {}
    dict_supply = {}
    dict_calc_demand = {}
    dict_calc_supply = {}
    for x in range(0,len(fuel_supply)):
        dict_supply[fuel_supply[x][0]] = fuel_supply[x][1]
        dict_calc_demand[fuel_supply[x][0]+1] = calc_fuel_demand[x][1]
        dict_calc_supply[fuel_supply[x][0]+1] = calc_fuel_supply[x][1]

    t = np.fromiter(dict_supply.keys(),dtype=float)
    for x in range(0,len(t)):
        dict_demand[t[x]] = 0 

    for x in range(0,len(fuel_supply)):
        for y in range(0,len(fuel_demand)):
            if fuel_demand[y][0] == fuel_supply[x][0]: 
                dict_demand[fuel_supply[x][0]] = fuel_demand[y][1] 


    return dict_demand, dict_supply, dict_calc_demand, dict_calc_supply



def plot_demand_supply(dict_demand, dict_supply, dict_calc_demand, dict_calc_supply,commod,test):

    fig, ax = plt.subplots(figsize=(15, 7))
    ax.plot(*zip(*sorted(dict_demand.items())),'*',label = 'Demand')
    ax.plot(*zip(*sorted(dict_supply.items())),'*',label = 'Supply')
    ax.plot(*zip(*sorted(dict_calc_demand.items())),'o',alpha = 0.5,label = 'Calculated Demand')
    ax.plot(*zip(*sorted(dict_calc_supply.items())),'o',alpha = 0.5,label = 'Calculated Supply')
    ax.grid()
    ax.set_xlabel('Time (month timestep)', fontsize=14)
    ax.set_ylabel('Mass (kg)' , fontsize=14)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
            handles,
            labels,
            fontsize=11,
            loc='upper center',
            bbox_to_anchor=(
                1.1,
                1.0),
            fancybox=True)
    ax.set_title('%s Demand Supply plot' % commod)
    plt.savefig(test, dpi=300,bbox_inches='tight')

def calculate_total_neg(dict_demand, dict_supply):
    diff = {}
    total = 0 
    num_negative = 0
    start = int(list(dict_demand.keys())[0]) 
    for x in range(start-1,len(dict_demand)):
        y = x+1
        diff[y] = dict_supply[y] -dict_demand[y]
        total = total + diff[y]
        if diff[y] < 0: 
            num_negative = num_negative + 1

    return total, num_negative

def find_best(dict_total,dict_negative): 
    maximum_dict_total = dict_total[max(dict_total, key=dict_total.get)]
    maximum_dict_negative = dict_negative[max(dict_negative, key=dict_negative.get)]

    if maximum_dict_negative ==0: 
        maximum_dict_negative = 1

    normalized_dict_total = {}
    normalized_dict_negative = {}
    score = {}
    for x in range(0,len(dict_total)): 
        normalized_dict_total[x] = dict_total[x]/maximum_dict_total
        normalized_dict_negative[x] = dict_negative[x]/maximum_dict_negative
        score[x] = normalized_dict_total[x] + normalized_dict_negative[x]

    best_calc_method = min(score, key=score.get)
    return best_calc_method, score 