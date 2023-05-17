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
independence = Variable('independence')
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
alone_avail = Variable('alone_avail')
with_mom_dad_avail = Variable('with_mom_dad_avail')
with_mom_avail = Variable('with_mom_avail')
with_dad_avail = Variable('with_dad_avail')
with_non_hh_avail = Variable('with_non_hh_avail')
with_sib_avail = Variable('with_sib_avail')

# Define parameters to be estimated

# alternative specific constants (mom is reference case)
asc_mom = Beta('asc_mom', 0, None, None, 1)
asc_alone = Beta('asc_alone', 0, None, None, 0)
asc_MomDad = Beta('asc_MomDad', 0, None, None, 0)
asc_dad = Beta('asc_dad', 0, None, None, 0)
asc_non_hh = Beta('asc_non_hh', 0, None, None, 0)
asc_sib = Beta('asc_sib', 0, None, None, 0)

# mom betas (not estimated for reference case)
b_log_income_k_mom = Beta('b_log_income_k_mom', 0, None, None, 1)
b_veh_per_driver_mom = Beta('b_veh_per_driver_mom', 0, None, None, 1)
b_non_work_mom_mom = Beta('b_non_work_mom_mom', 0, None, None, 1)
b_non_work_dad_mom = Beta('b_non_work_dad_mom', 0, None, None, 1)

b_age_mom = Beta('b_age_mom', 0, None, None, 1)
b_female_mom = Beta('b_female_mom', 0, None, None, 1)
b_has_lil_sib_mom = Beta('b_has_lil_sib_mom', 0, None, None, 1)
b_has_big_sib_mom = Beta('b_has_big_sib_mom', 0, None, None, 1)

b_log_density_mom = Beta('b_log_density_mom', 0, None, None, 1)
b_log_distance_mom = Beta('b_log_distance_mom', 0, None, None, 1)

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

# betas for with both parents
b_log_income_k_MomDad = Beta('b_log_income_k_MomDad', 0, None, None, 0)
b_veh_per_driver_MomDad = Beta('b_veh_per_driver_MomDad', 0, None, None, 0)
b_non_work_mom_MomDad = Beta('b_non_work_mom_MomDad', 0, None, None, 0)
b_non_work_dad_MomDad = Beta('b_non_work_dad_MomDad', 0, None, None, 0)

b_age_MomDad = Beta('b_age_MomDad', 0, None, None, 0)
b_female_MomDad = Beta('b_female_MomDad', 0, None, None, 0)
b_has_lil_sib_MomDad = Beta('b_has_lil_sib_MomDad', 0, None, None, 0)
b_has_big_sib_MomDad = Beta('b_has_big_sib_MomDad', 0, None, None, 0)

b_log_density_MomDad = Beta('b_log_density_MomDad', 0, None, None, 0)
b_log_distance_MomDad = Beta('b_log_distance_MomDad', 0, None, None, 0)

# betas for with dad
b_log_income_k_dad = Beta('b_log_income_k_dad', 0, None, None, 0)
b_veh_per_driver_dad = Beta('b_veh_per_driver_dad', 0, None, None, 0)
b_non_work_mom_dad = Beta('b_non_work_mom_dad', 0, None, None, 0)
b_non_work_dad_dad = Beta('b_non_work_dad_dad', 0, None, None, 0)

b_age_dad = Beta('b_age_dad', 0, None, None, 0)
b_female_dad = Beta('b_female_dad', 0, None, None, 0)
b_has_lil_sib_dad = Beta('b_has_lil_sib_dad', 0, None, None, 0)
b_has_big_sib_dad = Beta('b_has_big_sib_dad', 0, None, None, 0)

b_log_density_dad = Beta('b_log_density_dad', 0, None, None, 0)
b_log_distance_dad = Beta('b_log_distance_dad', 0, None, None, 0)

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

# betas for with sibling
b_log_income_k_sib = Beta('b_log_income_k_sib', 0, None, None, 0)
b_veh_per_driver_sib = Beta('b_veh_per_driver_sib', 0, None, None, 0)
b_non_work_mom_sib = Beta('b_non_work_mom_sib', 0, None, None, 0)
b_non_work_dad_sib = Beta('b_non_work_dad_sib', 0, None, None, 0)

b_age_sib = Beta('b_age_sib', 0, None, None, 0)
b_female_sib = Beta('b_female_sib', 0, None, None, 0)
b_has_lil_sib_sib = Beta('b_has_lil_sib_sib', 0, None, None, 0)
b_has_big_sib_sib = Beta('b_has_big_sib_sib', 0, None, None, 0)

b_log_density_sib = Beta('b_log_density_sib', 0, None, None, 0)
b_log_distance_sib = Beta('b_log_distance_sib', 0, None, None, 0)

# Define utility functions
V_mom = (
    asc_mom +
    b_log_income_k_mom * log_income_k +
    b_veh_per_driver_mom * veh_per_driver +
    b_non_work_mom_mom * non_work_mom +
    b_non_work_dad_mom * non_work_dad +
    b_age_mom * age +
    b_female_mom * female +
    b_has_lil_sib_mom * has_lil_sib +
    b_has_big_sib_mom * has_big_sib +
    b_log_density_mom * log_density +
    b_log_distance_mom * log_distance
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

V_MomDad = (
    asc_MomDad +
    b_log_income_k_MomDad * log_income_k +
    b_veh_per_driver_MomDad * veh_per_driver +
    b_non_work_mom_MomDad * non_work_mom +
    b_non_work_dad_MomDad * non_work_dad +
    b_age_MomDad * age +
    b_female_MomDad * female +
    b_has_lil_sib_MomDad * has_lil_sib +
    b_has_big_sib_MomDad * has_big_sib +
    b_log_density_MomDad * log_density +
    b_log_distance_MomDad * log_distance
)

V_dad = (
    asc_dad +
    b_log_income_k_dad * log_income_k +
    b_veh_per_driver_dad * veh_per_driver +
    b_non_work_mom_dad * non_work_mom +
    b_non_work_dad_dad * non_work_dad +
    b_age_dad * age +
    b_female_dad * female +
    b_has_lil_sib_dad * has_lil_sib +
    b_has_big_sib_dad * has_big_sib +
    b_log_density_dad * log_density +
    b_log_distance_dad * log_distance
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

V_sib = (
    asc_sib +
    b_log_income_k_sib * log_income_k +
    b_veh_per_driver_sib * veh_per_driver +
    b_non_work_mom_sib * non_work_mom +
    b_non_work_dad_sib * non_work_dad +
    b_age_sib * age +
    b_female_sib * female +
    b_has_lil_sib_sib * has_lil_sib +
    b_has_big_sib_sib * has_big_sib +
    b_log_density_sib * log_density +
    b_log_distance_sib * log_distance
)

# Associate utility functions with alternative numbers
V = {10: V_alone,
     21: V_MomDad,
     22: V_mom,
     23: V_dad,
     24: V_non_hh,
     30: V_sib}

# Associate availability variables with alternatives
av = {10: alone_avail,
      21: with_mom_dad_avail,
      22: with_mom_avail,
      23: with_dad_avail,
      24: with_non_hh_avail,
      30: with_sib_avail}

# Define the model
indy_model = models.loglogit(V, av, independence)

# Create Biogeme object for estimation
indy_biogeme_est = bio.BIOGEME(database_est, indy_model)
indy_biogeme_est.modelName = 'indy_model_est'

# Calculate null log likelihood for reporting
indy_biogeme_est.calculateNullLoglikelihood(av)

# Estimate parameters
results = indy_biogeme_est.estimate()
print(results.shortSummary())

# Get results in a pandas table
pandas_results = results.getEstimatedParameters()
print(pandas_results)

# Save parameters to csv
pandas_results.to_csv('biogeme_parameters_indy.csv')

# Generate predictions
prob_alone = models.logit(V, av, 10)
prob_mom_dad = models.logit(V, av, 21)
prob_mom = models.logit(V, av, 22)
prob_dad = models.logit(V, av, 23)
prob_non_hh = models.logit(V, av, 24)
prob_sib = models.logit(V, av, 30)

simulate = {'Prob. alone': prob_alone,
            'Prob. mom and dad': prob_mom_dad,
            'Prob. mom': prob_mom,
            'Prob. dad': prob_dad,
            'Prob. non-hh': prob_non_hh,
            'Prob. sibling': prob_sib}

# Create biogeme object for simulation
indy_biogeme_sim = bio.BIOGEME(database_sim, simulate)
indy_biogeme_sim.modelName = "predictions"

betaValues = results.getBetaValues ()
simulatedValues = indy_biogeme_sim.simulate(betaValues)

simulatedValues.to_csv('biogeme_preds_indy.csv')

mom_prob_summary = simulatedValues[["Prob. mom"]].describe()

## 99% probability of mom in all cases?
print(mom_prob_summary)