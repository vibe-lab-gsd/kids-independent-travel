"""
Try estimating a model for choice of independence and mode
"""

import pandas as pd

import biogeme.biogeme as bio
from biogeme import models
from biogeme.expressions import Beta
import biogeme.database as db
from biogeme.expressions import Variable

from pyprojroot.here import here

# Read in data for both model estimation and simulation
df_est = pd.read_csv(here('data/only-school/usa-2017.dat'), sep='\t')
df_sim = pd.read_csv(here('data/only-school/usa-2017-test.dat'), sep='\t')

# Set up biogeme databases
database_est = db.Database('est', df_est)
database_sim= db.Database('test', df_sim)

# Define variables for biogeme
mode = Variable('mode')
veh_per_driver = Variable('veh_per_driver')
non_work_mom = Variable('non_work_mom')
non_work_dad = Variable('non_work_dad')
age = Variable('age')
female = Variable('female')
has_lil_sib = Variable('has_lil_sib')
has_big_sib = Variable('has_big_sib')
log_income_k = Variable('log_income_k')
log_distance = Variable('log_distance')
log_density = Variable('log_density')

# Define parameters to be estimated

# alternative specific constants (car is reference case)
asc_car = Beta('asc_car', 0, None, None, 1)
asc_walk = Beta('asc_walk', 0, None, None, 0)
asc_bike = Beta('asc_bike', 0, None, None, 0)

# car betas (not estimated for reference case)
b_log_income_k_car = Beta('b_log_income_k_car', 0, None, None, 1)
b_veh_per_driver_car = Beta('b_veh_per_driver_car', 0, None, None, 1)
b_non_work_mom_car = Beta('b_non_work_mom_car', 0, None, None, 1)
b_non_work_dad_car = Beta('b_non_work_dad_car', 0, None, None, 1)

b_age_car = Beta('b_age_car', 0, None, None, 1)
b_female_car = Beta('b_female_car', 0, None, None, 1)
b_has_lil_sib_car = Beta('b_has_lil_sib_car', 0, None, None, 1)
b_has_big_sib_car = Beta('b_has_big_sib_car', 0, None, None, 1)

b_log_density_car = Beta('b_log_density_car', 0, None, None, 1)
b_log_distance_car = Beta('b_log_distance_car', 0, None, None, 1)

# walk betas
b_log_income_k_walk = Beta('b_log_income_k_adult_walk', 0, None, None, 0)
b_veh_per_driver_walk = Beta('b_veh_per_driver_adult_walk', 0, None, None, 0)
b_non_work_mom_walk = Beta('b_non_work_mom_adult_walk', 0, None, None, 0)
b_non_work_dad_walk = Beta('b_non_work_dad_adult_walk', 0, None, None, 0)

b_age_walk = Beta('b_age_walk', 0, None, None, 0)
b_female_walk = Beta('b_female_walk', 0, None, None, 0)
b_has_lil_sib_walk = Beta('b_has_lil_sib_walk', 0, None, None, 0)
b_has_big_sib_walk = Beta('b_has_big_sib_walk', 0, None, None, 0)

b_log_density_walk = Beta('b_log_density_walk', 0, None, None, 0)
b_log_distance_walk = Beta('b_log_distance_walk', 0, None, None, 0)

# bike betas
b_log_income_k_bike = Beta('b_log_income_k_bike', 0, None, None, 0)
b_veh_per_driver_bike = Beta('b_veh_per_driver_bike', 0, None, None, 0)
b_non_work_mom_bike = Beta('b_non_work_mom_bike', 0, None, None, 0)
b_non_work_dad_bike = Beta('b_non_work_dad_bike', 0, None, None, 0)

b_age_bike = Beta('b_age_bike', 0, None, None, 0)
b_female_bike = Beta('b_female_bike', 0, None, None, 0)
b_has_lil_sib_bike = Beta('b_has_lil_sib_bike', 0, None, None, 0)
b_has_big_sib_bike = Beta('b_has_big_sib_bike', 0, None, None, 0)

b_log_density_bike = Beta('b_log_density_bike', 0, None, None, 0)
b_log_distance_bike = Beta('b_log_distance_bike', 0, None, None, 0)

# Define utility functions
V_car = (
    asc_car +
    b_log_income_k_car * log_income_k +
    b_veh_per_driver_car * veh_per_driver +
    b_non_work_mom_car * non_work_mom +
    b_non_work_dad_car * non_work_dad +
    b_age_car * age +
    b_female_car * female +
    b_has_lil_sib_car * has_lil_sib +
    b_has_big_sib_car * has_big_sib +
    b_log_density_car * log_density +
    b_log_distance_car * log_distance
)

V_walk = (
    asc_walk +
    b_log_income_k_walk * log_income_k +
    b_veh_per_driver_walk * veh_per_driver +
    b_non_work_mom_walk * non_work_mom +
    b_non_work_dad_walk * non_work_dad +
    b_age_walk * age +
    b_female_walk * female +
    b_has_lil_sib_walk * has_lil_sib +
    b_has_big_sib_walk * has_big_sib +
    b_log_density_walk * log_density +
    b_log_distance_walk * log_distance
)

V_bike = (
    asc_bike +
    b_log_income_k_bike * log_income_k +
    b_veh_per_driver_bike * veh_per_driver +
    b_non_work_mom_bike * non_work_mom +
    b_non_work_dad_bike * non_work_dad +
    b_age_bike * age +
    b_female_bike * female +
    b_has_lil_sib_bike * has_lil_sib +
    b_has_big_sib_bike * has_big_sib +
    b_log_density_bike * log_density +
    b_log_distance_bike * log_distance
)

# Associate utility functions with alternative numbers
V = {7: V_car,
     8: V_walk,
     9: V_bike}

# Associate availability variables with alternatives
av = {7: 1,
      8: 1,
      9: 1}

# Define the model
mode_model = models.loglogit(V, av, mode)

# Create Biogeme object for estimation
mode_biogeme_est = bio.BIOGEME(database_est, mode_model)
mode_biogeme_est.modelName = 'mode_model_est'

# Calculate null log likelihood for reporting
mode_biogeme_est.calculateNullLoglikelihood(av)

# Estimate parameters
results = mode_biogeme_est.estimate()

# Generate predictions
prob_car = models.logit(V, av, 7)
prob_walk = models.logit(V, av, 8)
prob_bike = models.logit(V, av, 9)

simulate = {'Prob. car': prob_car,
            'Prob. walk': prob_walk,
            'Prob. bike': prob_bike}

# Create biogeme object for simulation
mode_biogeme_sim = bio.BIOGEME(database_sim, simulate)
mode_biogeme_sim.modelName = "predictions"

betaValues = results.getBetaValues ()
simulatedValues = mode_biogeme_sim.simulate(betaValues)

simulatedValues.to_csv('biogeme_preds_mode.csv')

car_prob_summary = simulatedValues[["Prob. car"]].describe()

print(car_prob_summary)