"""
Try estimating a choice of indedpendence model
"""

import pandas as pd

import biogeme.biogeme as bio
from biogeme import models
from biogeme.expressions import Beta
import biogeme.database as db
from biogeme.expressions import Variable

from pyprojroot.here import here

# Read in data for both model estimation and simulation
df_est = pd.read_csv(here('data/usa-2017.dat'), sep='\t')
df_sim = pd.read_csv(here('data/usa-2017-test.dat'), sep='\t')

# Set up biogeme databases
database_est = db.Database('est', df_est)
database_sim= db.Database('test', df_sim)

# Define variables for biogeme
ind_3_alt = Variable('ind_3_alt')
veh_per_driver = Variable('veh_per_driver')
n_adults = Variable('n_adults')
non_work_mom = Variable('non_work_mom')
non_work_dad = Variable('non_work_dad')
age = Variable('age')
female = Variable('female')
has_lil_sib = Variable('has_lil_sib')
has_big_sib = Variable('has_big_sib')
log_income_k = Variable('log_income_k')
log_distance = Variable('log_distance')
log_density = Variable('log_density')
alone_avail = Variable('alone_avail')
with_adult_avail = Variable('with_adult_avail')
with_non_hh_avail = Variable('with_non_hh_avail')

# Define parameters to be estimated

# alternative specific constants (mom is reference case)
asc_adult = Beta('asc_mom', 0, None, None, 1)
asc_alone = Beta('asc_alone', 0, None, None, 0)
asc_kid = Beta('asc_kid', 0, None, None, 0)

# adult betas (not estimated for reference case)
b_log_income_k_adult = Beta('b_log_income_k_adult', 0, None, None, 1)
b_veh_per_driver_adult = Beta('b_veh_per_driver_adult', 0, None, None, 1)
b_n_adults_adult = Beta('b_n_adults_adult', 0, None, None, 1)
b_non_work_mom_adult = Beta('b_non_work_mom_adult', 0, None, None, 1)
b_non_work_dad_adult = Beta('b_non_work_dad_adult', 0, None, None, 1)

b_age_adult = Beta('b_age_adult', 0, None, None, 1)
b_female_adult = Beta('b_female_adult', 0, None, None, 1)
b_has_lil_sib_adult = Beta('b_has_lil_sib_adult', 0, None, None, 1)
b_has_big_sib_adult = Beta('b_has_big_sib_adult', 0, None, None, 1)

b_log_density_adult = Beta('b_log_density_adult', 0, None, None, 1)
b_log_distance_adult = Beta('b_log_distance_adult', 0, None, None, 1)

# alone betas
b_log_income_k_alone = Beta('b_log_income_k_alone', 0, None, None, 0)
b_veh_per_driver_alone = Beta('b_veh_per_driver_alone', 0, None, None, 0)
b_n_adults_alone = Beta('b_n_adults_alone', 0, None, None, 0)
b_non_work_mom_alone = Beta('b_non_work_mom_alone', 0, None, None, 0)
b_non_work_dad_alone = Beta('b_non_work_dad_alone', 0, None, None, 0)

b_age_alone = Beta('b_age_alone', 0, None, None, 0)
b_female_alone = Beta('b_female_alone', 0, None, None, 0)
b_has_lil_sib_alone = Beta('b_has_lil_sib_alone', 0, None, None, 0)
b_has_big_sib_alone = Beta('b_has_big_sib_alone', 0, None, None, 0)

b_log_density_alone = Beta('b_log_density_alone', 0, None, None, 0)
b_log_distance_alone = Beta('b_log_distance_alone', 0, None, None, 0)

# betas for with kid
b_log_income_k_kid = Beta('b_log_income_k_kid', 0, None, None, 0)
b_veh_per_driver_kid = Beta('b_veh_per_driver_kid', 0, None, None, 0)
b_n_adults_kid = Beta('b_n_adults_kid', 0, None, None, 0)
b_non_work_mom_kid = Beta('b_non_work_mom_kid', 0, None, None, 0)
b_non_work_dad_kid = Beta('b_non_work_dad_kid', 0, None, None, 0)

b_age_kid = Beta('b_age_kid', 0, None, None, 0)
b_female_kid = Beta('b_female_kid', 0, None, None, 0)
b_has_lil_sib_kid = Beta('b_has_lil_sib_kid', 0, None, None, 0)
b_has_big_sib_kid = Beta('b_has_big_sib_kid', 0, None, None, 0)

b_log_density_kid = Beta('b_log_density_kid', 0, None, None, 0)
b_log_distance_kid = Beta('b_log_distance_kid', 0, None, None, 0)

# Define utility functions
V_adult = (
    asc_adult +
    b_log_income_k_adult * log_income_k +
    b_veh_per_driver_adult * veh_per_driver +
    b_n_adults_adult * n_adults +
    b_non_work_mom_adult * non_work_mom +
    b_non_work_dad_adult * non_work_dad +
    b_age_adult * age +
    b_female_adult * female +
    b_has_lil_sib_adult * has_lil_sib +
    b_has_big_sib_adult * has_big_sib +
    b_log_density_adult * log_density +
    b_log_distance_adult * log_distance
)

V_alone = (
    asc_alone +
    b_log_income_k_alone * log_income_k +
    b_veh_per_driver_alone * veh_per_driver +
    b_n_adults_alone * n_adults +
    b_non_work_mom_alone * non_work_mom +
    b_non_work_dad_alone * non_work_dad +
    b_age_alone * age +
    b_female_alone * female +
    b_has_lil_sib_alone * has_lil_sib +
    b_has_big_sib_alone * has_big_sib +
    b_log_density_alone * log_density +
    b_log_distance_alone * log_distance
)

V_kid = (
    asc_kid +
    b_log_income_k_kid * log_income_k +
    b_veh_per_driver_kid * veh_per_driver +
    b_n_adults_kid * n_adults +
    b_non_work_mom_kid * non_work_mom +
    b_non_work_dad_kid * non_work_dad +
    b_age_kid * age +
    b_female_kid * female +
    b_has_lil_sib_kid * has_lil_sib +
    b_has_big_sib_kid * has_big_sib +
    b_log_density_kid * log_density +
    b_log_distance_kid * log_distance
)

# Associate utility functions with alternative numbers
V = {10: V_alone,
     20: V_adult,
     30: V_kid}

# Associate availability variables with alternatives
av = {10: alone_avail,
      20: with_adult_avail,
      30: with_non_hh_avail}

# Define the model
indy3_alt_model = models.loglogit(V, av, ind_3_alt)

# Create Biogeme object for estimation
indy3_alt_biogeme_est = bio.BIOGEME(database_est, indy3_alt_model)
indy3_alt_biogeme_est.modelName = 'indy3_alt_model_est'

# Calculate null log likelihood for reporting
indy3_alt_biogeme_est.calculateNullLoglikelihood(av)

# Estimate parameters
results = indy3_alt_biogeme_est.estimate()
print(results.shortSummary())

# Get results in a pandas table
pandas_results = results.getEstimatedParameters()
print(pandas_results)

# Save parameters to csv
pandas_results.to_csv('biogeme_parameters_indy3_alt.csv')

# Generate predictions
prob_alone = models.logit(V, av, 10)
prob_adult = models.logit(V, av, 20)
prob_kid = models.logit(V, av, 30)

simulate = {'Prob. alone': prob_alone,
            'Prob. adult': prob_adult,
            'Prob. kid': prob_kid}

# Create biogeme object for simulation
indy3_alt_biogeme_sim = bio.BIOGEME(database_sim, simulate)
indy3_alt_biogeme_sim.modelName = "predictions"

betaValues = results.getBetaValues ()
simulatedValues = indy3_alt_biogeme_sim.simulate(betaValues)

simulatedValues.to_csv('biogeme_preds_indy3_alt.csv')

adult_prob_summary = simulatedValues[["Prob. adult"]].describe()

## 99% probability of mom in all cases?
print(adult_prob_summary)