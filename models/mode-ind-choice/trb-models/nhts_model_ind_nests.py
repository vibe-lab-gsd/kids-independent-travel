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
mode_ind_3_alt = Variable('mode_ind_3_alt')
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

# alternative specific constants (car with adult is reference case)
asc_adult_car = Beta('asc_adult_car', 0, None, None, 1)
asc_non_hh_car = Beta('asc_non_hh_car', 0, None, None, 0)

asc_adult_walk = Beta('asc_adult_walk', 0, None, None, 0)
asc_alone_walk = Beta('asc_alone_walk', 0, None, None, 0)
asc_non_hh_walk = Beta('asc_non_hh_walk', 0, None, None, 0)

asc_adult_bike = Beta('asc_adult_bike', 0, None, None, 0)
asc_alone_bike = Beta('asc_alone_bike', 0, None, None, 0)
asc_non_hh_bike = Beta('asc_non_hh_bike', 0, None, None, 0)

# adult car betas (not estimated for reference case)
b_log_income_k_adult_car = Beta('b_log_income_k_adult_car', 0, None, None, 1)
b_veh_per_driver_adult_car = Beta('b_veh_per_driver_adult_car', 0, None, None, 1)
b_non_work_mom_adult_car = Beta('b_non_work_mom_adult_car', 0, None, None, 1)
b_non_work_dad_adult_car = Beta('b_non_work_dad_adult_car', 0, None, None, 1)

b_age_adult_car = Beta('b_age_adult_car', 0, None, None, 1)
b_female_adult_car = Beta('b_female_adult_car', 0, None, None, 1)
b_has_lil_sib_adult_car = Beta('b_has_lil_sib_adult_car', 0, None, None, 1)
b_has_big_sib_adult_car = Beta('b_has_big_sib_adult_car', 0, None, None, 1)

b_log_density_adult_car = Beta('b_log_density_adult_car', 0, None, None, 1)
b_log_distance_adult_car = Beta('b_log_distance_adult_car', 0, None, None, 1)

# betas for with non-hh car
b_log_income_k_non_hh_car = Beta('b_log_income_k_non_hh_car', 0, None, None, 0)
b_veh_per_driver_non_hh_car = Beta('b_veh_per_driver_non_hh_car', 0, None, None, 0)
b_non_work_mom_non_hh_car = Beta('b_non_work_mom_non_hh_car', 0, None, None, 0)
b_non_work_dad_non_hh_car = Beta('b_non_work_dad_non_hh_car', 0, None, None, 0)

b_age_non_hh_car = Beta('b_age_non_hh_car', 0, None, None, 0)
b_female_non_hh_car = Beta('b_female_non_hh_car', 0, None, None, 0)
b_has_lil_sib_non_hh_car = Beta('b_has_lil_sib_non_hh_car', 0, None, None, 0)
b_has_big_sib_non_hh_car = Beta('b_has_big_sib_non_hh_car', 0, None, None, 0)

b_log_density_non_hh_car = Beta('b_log_density_non_hh_car', 0, None, None, 0)
b_log_distance_non_hh_car = Beta('b_log_distance_non_hh_car', 0, None, None, 0)

# adult walk betas
b_log_income_k_adult_walk = Beta('b_log_income_k_adult_walk', 0, None, None, 0)
b_veh_per_driver_adult_walk = Beta('b_veh_per_driver_adult_walk', 0, None, None, 0)
b_non_work_mom_adult_walk = Beta('b_non_work_mom_adult_walk', 0, None, None, 0)
b_non_work_dad_adult_walk = Beta('b_non_work_dad_adult_walk', 0, None, None, 0)

b_age_adult_walk = Beta('b_age_adult_walk', 0, None, None, 0)
b_female_adult_walk = Beta('b_female_adult_walk', 0, None, None, 0)
b_has_lil_sib_adult_walk = Beta('b_has_lil_sib_adult_walk', 0, None, None, 0)
b_has_big_sib_adult_walk = Beta('b_has_big_sib_adult_walk', 0, None, None, 0)

b_log_density_adult_walk = Beta('b_log_density_adult_walk', 0, None, None, 0)
b_log_distance_adult_walk = Beta('b_log_distance_adult_walk', 0, None, None, 0)

# alone walk betas
b_log_income_k_alone_walk = Beta('b_log_income_k_alone_walk', 0, None, None, 0)
b_veh_per_driver_alone_walk = Beta('b_veh_per_driver_alone_walk', 0, None, None, 0)
b_non_work_mom_alone_walk = Beta('b_non_work_mom_alone_walk', 0, None, None, 0)
b_non_work_dad_alone_walk = Beta('b_non_work_dad_alone_walk', 0, None, None, 0)

b_age_alone_walk = Beta('b_age_alone_walk', 0, None, None, 0)
b_female_alone_walk = Beta('b_female_alone_walk', 0, None, None, 0)
b_has_lil_sib_alone_walk = Beta('b_has_lil_sib_alone_walk', 0, None, None, 0)
b_has_big_sib_alone_walk = Beta('b_has_big_sib_alone_walk', 0, None, None, 0)

b_log_density_alone_walk = Beta('b_log_density_alone_walk', 0, None, None, 0)
b_log_distance_alone_walk = Beta('b_log_distance_alone_walk', 0, None, None, 0)

# betas for with non-hh walk
b_log_income_k_non_hh_walk = Beta('b_log_income_k_non_hh_walk', 0, None, None, 0)
b_veh_per_driver_non_hh_walk = Beta('b_veh_per_driver_non_hh_walk', 0, None, None, 0)
b_non_work_mom_non_hh_walk = Beta('b_non_work_mom_non_hh_walk', 0, None, None, 0)
b_non_work_dad_non_hh_walk = Beta('b_non_work_dad_non_hh_walk', 0, None, None, 0)

b_age_non_hh_walk = Beta('b_age_non_hh_walk', 0, None, None, 0)
b_female_non_hh_walk = Beta('b_female_non_hh_walk', 0, None, None, 0)
b_has_lil_sib_non_hh_walk = Beta('b_has_lil_sib_non_hh_walk', 0, None, None, 0)
b_has_big_sib_non_hh_walk = Beta('b_has_big_sib_non_hh_walk', 0, None, None, 0)

b_log_density_non_hh_walk = Beta('b_log_density_non_hh_walk', 0, None, None, 0)
b_log_distance_non_hh_walk = Beta('b_log_distance_non_hh_walk', 0, None, None, 0)

# adult bike betas
b_log_income_k_adult_bike = Beta('b_log_income_k_adult_bike', 0, None, None, 0)
b_veh_per_driver_adult_bike = Beta('b_veh_per_driver_adult_bike', 0, None, None, 0)
b_non_work_mom_adult_bike = Beta('b_non_work_mom_adult_bike', 0, None, None, 0)
b_non_work_dad_adult_bike = Beta('b_non_work_dad_adult_bike', 0, None, None, 0)

b_age_adult_bike = Beta('b_age_adult_bike', 0, None, None, 0)
b_female_adult_bike = Beta('b_female_adult_bike', 0, None, None, 0)
b_has_lil_sib_adult_bike = Beta('b_has_lil_sib_adult_bike', 0, None, None, 0)
b_has_big_sib_adult_bike = Beta('b_has_big_sib_adult_bike', 0, None, None, 0)

b_log_density_adult_bike = Beta('b_log_density_adult_bike', 0, None, None, 0)
b_log_distance_adult_bike = Beta('b_log_distance_adult_bike', 0, None, None, 0)

# alone bike betas
b_log_income_k_alone_bike = Beta('b_log_income_k_alone_bike', 0, None, None, 0)
b_veh_per_driver_alone_bike = Beta('b_veh_per_driver_alone_bike', 0, None, None, 0)
b_non_work_mom_alone_bike = Beta('b_non_work_mom_alone_bike', 0, None, None, 0)
b_non_work_dad_alone_bike = Beta('b_non_work_dad_alone_bike', 0, None, None, 0)

b_age_alone_bike = Beta('b_age_alone_bike', 0, None, None, 0)
b_female_alone_bike = Beta('b_female_alone_bike', 0, None, None, 0)
b_has_lil_sib_alone_bike = Beta('b_has_lil_sib_alone_bike', 0, None, None, 0)
b_has_big_sib_alone_bike = Beta('b_has_big_sib_alone_bike', 0, None, None, 0)

b_log_density_alone_bike = Beta('b_log_density_alone_bike', 0, None, None, 0)
b_log_distance_alone_bike = Beta('b_log_distance_alone_bike', 0, None, None, 0)

# betas for with non-hh bike
b_log_income_k_non_hh_bike = Beta('b_log_income_k_non_hh_bike', 0, None, None, 0)
b_veh_per_driver_non_hh_bike = Beta('b_veh_per_driver_non_hh_bike', 0, None, None, 0)
b_non_work_mom_non_hh_bike = Beta('b_non_work_mom_non_hh_bike', 0, None, None, 0)
b_non_work_dad_non_hh_bike = Beta('b_non_work_dad_non_hh_bike', 0, None, None, 0)

b_age_non_hh_bike = Beta('b_age_non_hh_bike', 0, None, None, 0)
b_female_non_hh_bike = Beta('b_female_non_hh_bike', 0, None, None, 0)
b_has_lil_sib_non_hh_bike = Beta('b_has_lil_sib_non_hh_bike', 0, None, None, 0)
b_has_big_sib_non_hh_bike = Beta('b_has_big_sib_non_hh_bike', 0, None, None, 0)

b_log_density_non_hh_bike = Beta('b_log_density_non_hh_walk', 0, None, None, 0)
b_log_distance_non_hh_bike = Beta('b_log_distance_non_hh_bike', 0, None, None, 0)

# Define utility functions
V_adult_car = (
    asc_adult_car +
    b_log_income_k_adult_car * log_income_k +
    b_veh_per_driver_adult_car * veh_per_driver +
    b_non_work_mom_adult_car * non_work_mom +
    b_non_work_dad_adult_car * non_work_dad +
    b_age_adult_car * age +
    b_female_adult_car * female +
    b_has_lil_sib_adult_car * has_lil_sib +
    b_has_big_sib_adult_car * has_big_sib +
    b_log_density_adult_car * log_density +
    b_log_distance_adult_car * log_distance
)

V_non_hh_car = (
    asc_non_hh_car +
    b_log_income_k_non_hh_car * log_income_k +
    b_veh_per_driver_non_hh_car * veh_per_driver +
    b_non_work_mom_non_hh_car * non_work_mom +
    b_non_work_dad_non_hh_car * non_work_dad +
    b_age_non_hh_car * age +
    b_female_non_hh_car * female +
    b_has_lil_sib_non_hh_car * has_lil_sib +
    b_has_big_sib_non_hh_car * has_big_sib +
    b_log_density_non_hh_car * log_density +
    b_log_distance_non_hh_car * log_distance
)

V_adult_walk = (
    asc_adult_walk +
    b_log_income_k_adult_walk * log_income_k +
    b_veh_per_driver_adult_walk * veh_per_driver +
    b_non_work_mom_adult_walk * non_work_mom +
    b_non_work_dad_adult_walk * non_work_dad +
    b_age_adult_walk * age +
    b_female_adult_walk * female +
    b_has_lil_sib_adult_walk * has_lil_sib +
    b_has_big_sib_adult_walk * has_big_sib +
    b_log_density_adult_walk * log_density +
    b_log_distance_adult_walk * log_distance
)

V_alone_walk = (
    asc_alone_walk +
    b_log_income_k_alone_walk * log_income_k +
    b_veh_per_driver_alone_walk * veh_per_driver +
    b_non_work_mom_alone_walk * non_work_mom +
    b_non_work_dad_alone_walk * non_work_dad +
    b_age_alone_walk * age +
    b_female_alone_walk * female +
    b_has_lil_sib_alone_walk * has_lil_sib +
    b_has_big_sib_alone_walk * has_big_sib +
    b_log_density_alone_walk * log_density +
    b_log_distance_alone_walk * log_distance
)

V_non_hh_walk = (
    asc_non_hh_walk +
    b_log_income_k_non_hh_walk * log_income_k +
    b_veh_per_driver_non_hh_walk * veh_per_driver +
    b_non_work_mom_non_hh_walk * non_work_mom +
    b_non_work_dad_non_hh_walk * non_work_dad +
    b_age_non_hh_walk * age +
    b_female_non_hh_walk * female +
    b_has_lil_sib_non_hh_walk * has_lil_sib +
    b_has_big_sib_non_hh_walk * has_big_sib +
    b_log_density_non_hh_walk * log_density +
    b_log_distance_non_hh_walk * log_distance
)

V_adult_bike = (
    asc_adult_bike +
    b_log_income_k_adult_bike * log_income_k +
    b_veh_per_driver_adult_bike * veh_per_driver +
    b_non_work_mom_adult_bike * non_work_mom +
    b_non_work_dad_adult_bike * non_work_dad +
    b_age_adult_bike * age +
    b_female_adult_bike * female +
    b_has_lil_sib_adult_bike * has_lil_sib +
    b_has_big_sib_adult_bike * has_big_sib +
    b_log_density_adult_bike * log_density +
    b_log_distance_adult_bike * log_distance
)

V_alone_bike = (
    asc_alone_bike +
    b_log_income_k_alone_bike * log_income_k +
    b_veh_per_driver_alone_bike * veh_per_driver +
    b_non_work_mom_alone_bike * non_work_mom +
    b_non_work_dad_alone_bike * non_work_dad +
    b_age_alone_bike * age +
    b_female_alone_bike * female +
    b_has_lil_sib_alone_bike * has_lil_sib +
    b_has_big_sib_alone_bike * has_big_sib +
    b_log_density_alone_bike * log_density +
    b_log_distance_alone_bike * log_distance
)

V_non_hh_bike = (
    asc_non_hh_bike +
    b_log_income_k_non_hh_bike * log_income_k +
    b_veh_per_driver_non_hh_bike * veh_per_driver +
    b_non_work_mom_non_hh_bike * non_work_mom +
    b_non_work_dad_non_hh_bike * non_work_dad +
    b_age_non_hh_bike * age +
    b_female_non_hh_bike * female +
    b_has_lil_sib_non_hh_bike * has_lil_sib +
    b_has_big_sib_non_hh_bike * has_big_sib +
    b_log_density_non_hh_bike * log_density +
    b_log_distance_non_hh_bike * log_distance
)

# Associate utility functions with alternative numbers
V = {720: V_adult_car,
     730: V_non_hh_car,
     810: V_alone_walk,
     820: V_adult_walk,
     830: V_non_hh_walk,
     910: V_alone_bike,
     920: V_adult_bike,
     930: V_non_hh_bike}

# Associate availability variables with alternatives
av = {720: 1,
      730: 1,
      810: 1,
      820: 1,
      830: 1,
      910: 1,
      920: 1,
      930: 1}

#Definition of nests:
# 1: nests parameter
# 2: list of alternatives
nest_alone = Beta('nest_alone', 1, 1.0, None, 0)
nest_adult = Beta('nest_adult', 1, 1.0, None, 0)
nest_non_hh = Beta('nest_non_hh', 1, 1.0, None, 0)

alone = nest_alone , [810, 910]
adult = nest_adult , [720, 820, 920]
non_hh = nest_non_hh , [730, 830, 930]

nests = alone, adult, non_hh

# Define the model
ind_nests_model = models.lognested(V, av, nests, mode_ind_3_alt)

# Create Biogeme object for estimation
ind_nests_biogeme_est = bio.BIOGEME(database_est, ind_nests_model)
ind_nests_biogeme_est.modelName = 'ind_nests_model_est'

# Calculate null log likelihood for reporting
ind_nests_biogeme_est.calculateNullLoglikelihood(av)

# Estimate parameters
results = ind_nests_biogeme_est.estimate()
print(results.shortSummary())

# Get results in a pandas table
pandas_results = results.getEstimatedParameters()
print(pandas_results)

# Save parameters to csv
pandas_results.to_csv('biogeme_parameters_ind_nests.csv')

# Generate predictions
prob_adult_car = models.nested(V, av, nests, 720)
prob_non_hh_car = models.nested(V, av, nests, 730)

prob_alone_walk = models.nested(V, av, nests, 810)
prob_adult_walk = models.nested(V, av, nests, 820)
prob_non_hh_walk = models.nested(V, av, nests, 830)

prob_alone_bike = models.nested(V, av, nests, 910)
prob_adult_bike = models.nested(V, av, nests, 920)
prob_non_hh_bike = models.nested(V, av, nests, 930)

simulate = {'Prob. adult car': prob_adult_car,
            'Prob. non-hh car': prob_non_hh_car,
            'Prob. alone walk': prob_alone_walk,
            'Prob. adult walk': prob_adult_walk,
            'Prob. non-hh walk': prob_non_hh_walk,
            'Prob. alone bike': prob_alone_bike,
            'Prob. adult bike': prob_adult_bike,
            'Prob. non-hh bike': prob_non_hh_bike}

# Create biogeme object for simulation
ind_nests_biogeme_sim = bio.BIOGEME(database_sim, simulate)
ind_nests_biogeme_sim.modelName = "predictions"

betaValues = results.getBetaValues ()
simulatedValues = ind_nests_biogeme_sim.simulate(betaValues)

simulatedValues.to_csv('biogeme_preds_ind-nests.csv')

adult_car_prob_summary = simulatedValues[["Prob. adult car"]].describe()

print(adult_car_prob_summary)