# d3ploy
A collection of Cyclus manager archetypes for demand driven deployment. It operates using
global calls within a Cyclus simulation so that all agents within the simulation
can communicate. The goal of this package is to provide three types of mathematical
basis for determining supply and demand of commodities within Cyclus; Non-optimizing (NO)
deterministing optimization (DO), and Stochastic optimization (SO). 

Non-Optimizing
==============
There are two methods currently being considered for the NO models. Autoregressive
moving average (ARMA), and autoregressive conditional heteroskedasticity (ARCH).

ARMA
----
The autoregressive moving average method takes a time series and uses an 
auto regressive term and a moving average term. 

ARCH
----
Currently a work in progress

Deterministic Optimization
==========================
Currently a work in progress

Stochastic Optimization
=======================
Currently a work in progress


NO Instutition
==============
This represents the Non-Optimizing instition, included in this are the ARMA
and ARCH methods. Additionally a simple moving average calculation is included
with this archetype. The user chooses the method as part of the institution
input. 

The institution works by using the chosen method to predict supply and 
demand for given commodities. Each timestep the institution calculates a prediction
on the supply and demand for the next time step. If the demand exceeds the
supply it deploys facilities to ensure supply exceeds demand. Predictions are not
performed if the method chosen by the institution is 'moving average'. In this instance
the institution will schedule facilities for deployment only if there is a 
deficit in the current time step. 

Required Inputs
------------------
**demand_commod**: This is the commodity that is demanded of the institution.
Facilities outside of this insitution need this commodity and request it from
facilities inside of this institution. **NOTE** If 'power' is used as the 
**demand_commod**, the institution will calculate the demand using an exponential
growth curve and a grow rate of 2% by default. This growth rate is an optional 
input. 
**supply_commod**: This is the commodity that facilities inside of this institution
supply. 
**prototypes**: A oneOrMore of the prototypes available for the institution to deploy
to meet the demand for the demanded commodity.
**initial_demand**: This sets the initial demand of the demand commodity. If the
initial facilities at start up does not meet this demand the first time step will
see a undersupply. 
**calc_method**: This is the method used to calculate the supply and demand. 
Current available options are 'ARMA' and 'MA' for autoregressive moving average
and moving average. 

Optional Inputs
---------------
**growth_rate**: The growth rate used to calculate power if power is the 
**demand_commod**. Default: 0.02 (2%). 
**record**: A boolean flag used to set if an institution will dump a record
of its supply and demand values to a .txt file. The name of the file is the
**demand_commod**. Default: False.
**supply_std_dev**: The number of standard deviations off of the predicted supply
value to use as the predicted value. For example if the predicted value is 10
with a standard deviation of 2, +1 will result in a predicted value of 12 and 
-1 will result in a predicted value of 8. Default: 0
**demand_std_dev**: The number of standard deviations off of the predicted demand
value to use as the predicted value. For example if the predicted value is 10
with a standard deviation of 2, +1 will result in a predicted value of 12 and 
-1 will result in a predicted value of 8. Default: 0
**steps** This is the number of time steps forward the supply and demand will
be predicted. Default: 1. 

Demand Fac
==========

