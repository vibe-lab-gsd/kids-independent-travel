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
ind_3_alt = Variable('ind_3_alt')
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

# alternative specific constants (with adult is reference case)
asc_adult = Beta('asc_adult', 0, None, None, 1)
asc_non_hh = Beta('asc_non_hh', 0, None, None, 0)
asc_alone = Beta('asc_alone', 0, None, None, 0)

# adult betas (not estimated for reference case)
b_log_income_k_adult = Beta('b_log_income_k_adult', 0, None, None, 1)
b_veh_per_driver_adult = Beta('b_veh_per_driver_adult', 0, None, None, 1)
b_non_work_mom_adult = Beta('b_non_work_mom_adult', 0, None, None, 1)
b_non_work_dad_adult = Beta('b_non_work_dad_adult', 0, None, None, 1)

b_age_adult = Beta('b_age_adult', 0, None, None, 1)
b_female_adult = Beta('b_female_adult', 0, None, None, 1)
b_has_lil_sib_adult = Beta('b_has_lil_sib_adult', 0, None, None, 1)
b_has_big_sib_adult = Beta('b_has_big_sib_adult', 0, None, None, 1)

b_log_density_adult = Beta('b_log_density_adult', 0, None, None, 1)
b_log_distance_adult = Beta('b_log_distance_adult', 0, None, None, 1)

# betas for with non-hh
b_log_income_k_non_hh = Beta('b_log_income_k_non_hh', 0, None, None, 0)
b_veh_per_driver_non_hh = Beta('b_veh_per_driver_non_hh', 0, None, None, 0)
b_non_work_mom_non_hh = Beta('b_non_work_mom_non_hh', 0, None, None, 0)
b_non_work_dad_non_hh = Beta('b_non_work_dad_non_hh', 0, None, None, 0)

b_age_non_hh = Beta('b_age_non_hh', 0, None, None, 0)
b_female_non_hh = Beta('b_female_non_hh', 0, None, None, 0)
b_has_lil_sib_non_hh = Beta('b_has_lil_sib_non_hh', 0, None, None, 0)
b_has_big_sib_non_hh = Beta('b_has_big_sib_non_hh', 0, None, None, 0)

b_log_density_non_hh = Beta('b_log_density_non_hh', 0, None, None, 0)
b_log_distance_non_hh = Beta('b_log_distance_non_hh', 0, None, None, 0)

# alone betas
b_log_income_k_alone = Beta('b_log_income_k_alone', 0, None, None, 0)
b_veh_per_driver_alone = Beta('b_veh_per_driver_alone', 0, None, None, 0)
b_non_work_mom_alone = Beta('b_non_work_mom_alone', 0, None, None, 0)
b_non_work_dad_alone = Beta('b_non_work_dad_alone', 0, None, None, 0)

b_age_alone = Beta('b_age_alone', 0, None, None, 0)
b_female_alone = Beta('b_female_alone', 0, None, None, 0)
b_has_lil_sib_alone = Beta('b_has_lil_sib_alone', 0, None, None, 0)
b_has_big_sib_alone = Beta('b_has_big_sib_alone', 0, None, None, 0)

b_log_density_alone = Beta('b_log_density_alone', 0, None, None, 0)
b_log_distance_alone = Beta('b_log_distance_alone', 0, None, None, 0)


# Define utility functions
V_adult = (
    asc_adult +
    b_log_income_k_adult * log_income_k +
    b_veh_per_driver_adult * veh_per_driver +
    b_non_work_mom_adult * non_work_mom +
    b_non_work_dad_adult * non_work_dad +
    b_age_adult * age +
    b_female_adult * female +
    b_has_lil_sib_adult * has_lil_sib +
    b_has_big_sib_adult * has_big_sib +
    b_log_density_adult * log_density +
    b_log_distance_adult * log_distance
)

V_non_hh = (
    asc_non_hh +
    b_log_income_k_non_hh * log_income_k +
    b_veh_per_driver_non_hh * veh_per_driver +
    b_non_work_mom_non_hh * non_work_mom +
    b_non_work_dad_non_hh * non_work_dad +
    b_age_non_hh * age +
    b_female_non_hh * female +
    b_has_lil_sib_non_hh * has_lil_sib +
    b_has_big_sib_non_hh * has_big_sib +
    b_log_density_non_hh * log_density +
    b_log_distance_non_hh * log_distance
)

V_alone = (
    asc_alone +
    b_log_income_k_alone * log_income_k +
    b_veh_per_driver_alone * veh_per_driver +
    b_non_work_mom_alone * non_work_mom +
    b_non_work_dad_alone * non_work_dad +
    b_age_alone * age +
    b_female_alone * female +
    b_has_lil_sib_alone * has_lil_sib +
    b_has_big_sib_alone * has_big_sib +
    b_log_density_alone * log_density +
    b_log_distance_alone * log_distance
)

# Associate utility functions with alternative numbers
V = {20: V_adult,
     30: V_non_hh,
     10: V_alone}

# Associate availability variables with alternatives
av = {10: 1,
      20: 1,
      30: 1}

# Define the model
ind_model = models.loglogit(V, av, ind_3_alt)

# Create Biogeme object for estimation
ind_biogeme_est = bio.BIOGEME(database_est, ind_model)
ind_biogeme_est.modelName = 'ind_model_est'

# Calculate null log likelihood for reporting
ind_biogeme_est.calculateNullLoglikelihood(av)

# Estimate parameters
results = ind_biogeme_est.estimate()
print(results.shortSummary())

# Generate predictions
prob_adult = models.logit(V, av, 20)
prob_non_hh = models.logit(V, av, 30)
prob_alone = models.logit(V, av, 10)

simulate = {'Prob. adult': prob_adult,
            'Prob. non-hh': prob_non_hh,
            'Prob. alone': prob_alone}

# Create biogeme object for simulation
ind_biogeme_sim = bio.BIOGEME(database_sim, simulate)
ind_biogeme_sim.modelName = "predictions"

betaValues = results.getBetaValues ()
simulatedValues = ind_biogeme_sim.simulate(betaValues)

simulatedValues.to_csv('biogeme_preds_ind.csv')

adult_prob_summary = simulatedValues[["Prob. adult"]].describe()

print(adult_prob_summary)