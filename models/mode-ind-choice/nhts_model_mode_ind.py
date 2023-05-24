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
df_est = pd.read_csv(here('data/usa-2017.dat'), sep='\t')
df_sim = pd.read_csv(here('data/usa-2017-test.dat'), sep='\t')

# Set up biogeme databases
database_est = db.Database('est', df_est)
database_sim= db.Database('test', df_sim)

# Define variables for biogeme
mode_ind = Variable('mode_ind')
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

# alternative specific constants (car with mom is reference case)
asc_mom_car = Beta('asc_mom_car', 0, None, None, 1)
asc_MomDad_car = Beta('asc_MomDad_car', 0, None, None, 0)
asc_dad_car = Beta('asc_dad_car', 0, None, None, 0)
asc_non_hh_car = Beta('asc_non_hh_car', 0, None, None, 0)
asc_sib_car = Beta('asc_sib_car', 0, None, None, 0)

asc_mom_walk = Beta('asc_mom_walk', 0, None, None, 0)
asc_alone_walk = Beta('asc_alone_walk', 0, None, None, 0)
asc_MomDad_walk = Beta('asc_MomDad_walk', 0, None, None, 0)
asc_dad_walk = Beta('asc_dad_walk', 0, None, None, 0)
asc_non_hh_walk = Beta('asc_non_hh_walk', 0, None, None, 0)
asc_sib_walk = Beta('asc_sib_walk', 0, None, None, 0)

asc_mom_bike = Beta('asc_mom_bike', 0, None, None, 0)
asc_alone_bike = Beta('asc_alone_bike', 0, None, None, 0)
asc_MomDad_bike = Beta('asc_MomDad_bike', 0, None, None, 0)
asc_dad_bike = Beta('asc_dad_bike', 0, None, None, 0)
asc_non_hh_bike = Beta('asc_non_hh_bike', 0, None, None, 0)
asc_sib_bike = Beta('asc_sib_bike', 0, None, None, 0)

# mom car betas (not estimated for reference case)
b_log_income_k_mom_car = Beta('b_log_income_k_mom_car', 0, None, None, 1)
b_veh_per_driver_mom_car = Beta('b_veh_per_driver_mom_car', 0, None, None, 1)
b_non_work_mom_mom_car = Beta('b_non_work_mom_mom_car', 0, None, None, 1)
b_non_work_dad_mom_car = Beta('b_non_work_dad_mom_car', 0, None, None, 1)

b_age_mom_car = Beta('b_age_mom_car', 0, None, None, 1)
b_female_mom_car = Beta('b_female_mom_car', 0, None, None, 1)
b_has_lil_sib_mom_car = Beta('b_has_lil_sib_mom_car', 0, None, None, 1)
b_has_big_sib_mom_car = Beta('b_has_big_sib_mom_car', 0, None, None, 1)

b_log_density_mom_car = Beta('b_log_density_mom_car', 0, None, None, 1)
b_log_distance_mom_car = Beta('b_log_distance_mom_car', 0, None, None, 1)

# betas for with both parents car
b_log_income_k_MomDad_car = Beta('b_log_income_k_MomDad_car', 0, None, None, 0)
b_veh_per_driver_MomDad_car = Beta('b_veh_per_driver_MomDad_car', 0, None, None, 0)
b_non_work_mom_MomDad_car = Beta('b_non_work_mom_MomDad_car', 0, None, None, 0)
b_non_work_dad_MomDad_car = Beta('b_non_work_dad_MomDad_car', 0, None, None, 0)

b_age_MomDad_car = Beta('b_age_MomDad_car', 0, None, None, 0)
b_female_MomDad_car = Beta('b_female_MomDad_car', 0, None, None, 0)
b_has_lil_sib_MomDad_car = Beta('b_has_lil_sib_MomDad_car', 0, None, None, 0)
b_has_big_sib_MomDad_car = Beta('b_has_big_sib_MomDad_car', 0, None, None, 0)

b_log_density_MomDad_car = Beta('b_log_density_MomDad_car', 0, None, None, 0)
b_log_distance_MomDad_car = Beta('b_log_distance_MomDad_car', 0, None, None, 0)

# betas for with dad car
b_log_income_k_dad_car = Beta('b_log_income_k_dad_car', 0, None, None, 0)
b_veh_per_driver_dad_car = Beta('b_veh_per_driver_dad_car', 0, None, None, 0)
b_non_work_mom_dad_car = Beta('b_non_work_mom_dad_car', 0, None, None, 0)
b_non_work_dad_dad_car = Beta('b_non_work_dad_dad_car', 0, None, None, 0)

b_age_dad_car = Beta('b_age_dad_car', 0, None, None, 0)
b_female_dad_car = Beta('b_female_dad_car', 0, None, None, 0)
b_has_lil_sib_dad_car = Beta('b_has_lil_sib_dad_car', 0, None, None, 0)
b_has_big_sib_dad_car = Beta('b_has_big_sib_dad_car', 0, None, None, 0)

b_log_density_dad_car = Beta('b_log_density_dad_car', 0, None, None, 0)
b_log_distance_dad_car = Beta('b_log_distance_dad_car', 0, None, None, 0)

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

# betas for with sibling car
b_log_income_k_sib_car = Beta('b_log_income_k_sib_car', 0, None, None, 0)
b_veh_per_driver_sib_car = Beta('b_veh_per_driver_sib_car', 0, None, None, 0)
b_non_work_mom_sib_car = Beta('b_non_work_mom_sib_car', 0, None, None, 0)
b_non_work_dad_sib_car = Beta('b_non_work_dad_sib_car', 0, None, None, 0)

b_age_sib_car = Beta('b_age_sib_car', 0, None, None, 0)
b_female_sib_car = Beta('b_female_sib_car', 0, None, None, 0)
b_has_lil_sib_sib_car = Beta('b_has_lil_sib_sib_car', 0, None, None, 0)
b_has_big_sib_sib_car = Beta('b_has_big_sib_sib_car', 0, None, None, 0)

b_log_density_sib_car = Beta('b_log_density_sib_car', 0, None, None, 0)
b_log_distance_sib_car = Beta('b_log_distance_sib_car', 0, None, None, 0)

# mom walk betas
b_log_income_k_mom_walk = Beta('b_log_income_k_mom_walk', 0, None, None, 0)
b_veh_per_driver_mom_walk = Beta('b_veh_per_driver_mom_walk', 0, None, None, 0)
b_non_work_mom_mom_walk = Beta('b_non_work_mom_mom_walk', 0, None, None, 0)
b_non_work_dad_mom_walk = Beta('b_non_work_dad_mom_walk', 0, None, None, 0)

b_age_mom_walk = Beta('b_age_mom_walk', 0, None, None, 0)
b_female_mom_walk = Beta('b_female_mom_walk', 0, None, None, 0)
b_has_lil_sib_mom_walk = Beta('b_has_lil_sib_mom_walk', 0, None, None, 0)
b_has_big_sib_mom_walk = Beta('b_has_big_sib_mom_walk', 0, None, None, 0)

b_log_density_mom_walk = Beta('b_log_density_mom_walk', 0, None, None, 0)
b_log_distance_mom_walk = Beta('b_log_distance_mom_walk', 0, None, None, 0)

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

# betas for with both parents walk
b_log_income_k_MomDad_walk = Beta('b_log_income_k_MomDad_walk', 0, None, None, 0)
b_veh_per_driver_MomDad_walk = Beta('b_veh_per_driver_MomDad_walk', 0, None, None, 0)
b_non_work_mom_MomDad_walk = Beta('b_non_work_mom_MomDad_walk', 0, None, None, 0)
b_non_work_dad_MomDad_walk = Beta('b_non_work_dad_MomDad_walk', 0, None, None, 0)

b_age_MomDad_walk = Beta('b_age_MomDad_walk', 0, None, None, 0)
b_female_MomDad_walk = Beta('b_female_MomDad_walk', 0, None, None, 0)
b_has_lil_sib_MomDad_walk = Beta('b_has_lil_sib_MomDad_walk', 0, None, None, 0)
b_has_big_sib_MomDad_walk = Beta('b_has_big_sib_MomDad_walk', 0, None, None, 0)

b_log_density_MomDad_walk = Beta('b_log_density_MomDad_walk', 0, None, None, 0)
b_log_distance_MomDad_walk = Beta('b_log_distance_MomDad_walk', 0, None, None, 0)

# betas for with dad walk
b_log_income_k_dad_walk = Beta('b_log_income_k_dad_walk', 0, None, None, 0)
b_veh_per_driver_dad_walk = Beta('b_veh_per_driver_dad_walk', 0, None, None, 0)
b_non_work_mom_dad_walk = Beta('b_non_work_mom_dad_walk', 0, None, None, 0)
b_non_work_dad_dad_walk = Beta('b_non_work_dad_dad_walk', 0, None, None, 0)

b_age_dad_walk = Beta('b_age_dad_walk', 0, None, None, 0)
b_female_dad_walk = Beta('b_female_dad_walk', 0, None, None, 0)
b_has_lil_sib_dad_walk = Beta('b_has_lil_sib_dad_walk', 0, None, None, 0)
b_has_big_sib_dad_walk = Beta('b_has_big_sib_dad_walk', 0, None, None, 0)

b_log_density_dad_walk = Beta('b_log_density_dad_walk', 0, None, None, 0)
b_log_distance_dad_walk = Beta('b_log_distance_dad_walk', 0, None, None, 0)

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

# betas for with sibling walk
b_log_income_k_sib_walk = Beta('b_log_income_k_sib_walk', 0, None, None, 0)
b_veh_per_driver_sib_walk = Beta('b_veh_per_driver_sib_walk', 0, None, None, 0)
b_non_work_mom_sib_walk = Beta('b_non_work_mom_sib_walk', 0, None, None, 0)
b_non_work_dad_sib_walk = Beta('b_non_work_dad_sib_walk', 0, None, None, 0)

b_age_sib_walk = Beta('b_age_sib_walk', 0, None, None, 0)
b_female_sib_walk = Beta('b_female_sib_walk', 0, None, None, 0)
b_has_lil_sib_sib_walk = Beta('b_has_lil_sib_sib_walk', 0, None, None, 0)
b_has_big_sib_sib_walk = Beta('b_has_big_sib_sib_walk', 0, None, None, 0)

b_log_density_sib_walk = Beta('b_log_density_sib_walk', 0, None, None, 0)
b_log_distance_sib_walk = Beta('b_log_distance_sib_walk', 0, None, None, 0)

# mom bike betas
b_log_income_k_mom_bike = Beta('b_log_income_k_mom_bike', 0, None, None, 0)
b_veh_per_driver_mom_bike = Beta('b_veh_per_driver_mom_bike', 0, None, None, 0)
b_non_work_mom_mom_bike = Beta('b_non_work_mom_mom_bike', 0, None, None, 0)
b_non_work_dad_mom_bike = Beta('b_non_work_dad_mom_bike', 0, None, None, 0)

b_age_mom_bike = Beta('b_age_mom_bike', 0, None, None, 0)
b_female_mom_bike = Beta('b_female_mom_bike', 0, None, None, 0)
b_has_lil_sib_mom_bike = Beta('b_has_lil_sib_mom_bike', 0, None, None, 0)
b_has_big_sib_mom_bike = Beta('b_has_big_sib_mom_bike', 0, None, None, 0)

b_log_density_mom_bike = Beta('b_log_density_mom_bike', 0, None, None, 0)
b_log_distance_mom_bike = Beta('b_log_distance_mom_bike', 0, None, None, 0)

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

# betas for with both parents bike
b_log_income_k_MomDad_bike = Beta('b_log_income_k_MomDad_bike', 0, None, None, 0)
b_veh_per_driver_MomDad_bike = Beta('b_veh_per_driver_MomDad_bike', 0, None, None, 0)
b_non_work_mom_MomDad_bike = Beta('b_non_work_mom_MomDad_bike', 0, None, None, 0)
b_non_work_dad_MomDad_bike = Beta('b_non_work_dad_MomDad_bike', 0, None, None, 0)

b_age_MomDad_bike = Beta('b_age_MomDad_bike', 0, None, None, 0)
b_female_MomDad_bike = Beta('b_female_MomDad_bike', 0, None, None, 0)
b_has_lil_sib_MomDad_bike = Beta('b_has_lil_sib_MomDad_bike', 0, None, None, 0)
b_has_big_sib_MomDad_bike = Beta('b_has_big_sib_MomDad_bike', 0, None, None, 0)

b_log_density_MomDad_bike = Beta('b_log_density_MomDad_bike', 0, None, None, 0)
b_log_distance_MomDad_bike = Beta('b_log_distance_MomDad_bike', 0, None, None, 0)

# betas for with dad bike
b_log_income_k_dad_bike = Beta('b_log_income_k_dad_bike', 0, None, None, 0)
b_veh_per_driver_dad_bike = Beta('b_veh_per_driver_dad_bike', 0, None, None, 0)
b_non_work_mom_dad_bike = Beta('b_non_work_mom_dad_bike', 0, None, None, 0)
b_non_work_dad_dad_bike = Beta('b_non_work_dad_dad_bike', 0, None, None, 0)

b_age_dad_bike = Beta('b_age_dad_bike', 0, None, None, 0)
b_female_dad_bike = Beta('b_female_dad_bike', 0, None, None, 0)
b_has_lil_sib_dad_bike = Beta('b_has_lil_sib_dad_bike', 0, None, None, 0)
b_has_big_sib_dad_bike = Beta('b_has_big_sib_dad_bike', 0, None, None, 0)

b_log_density_dad_bike = Beta('b_log_density_dad_bike', 0, None, None, 0)
b_log_distance_dad_bike = Beta('b_log_distance_dad_bike', 0, None, None, 0)

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

# betas for with sibling walk
b_log_income_k_sib_bike = Beta('b_log_income_k_sib_bike', 0, None, None, 0)
b_veh_per_driver_sib_bike = Beta('b_veh_per_driver_sib_bike', 0, None, None, 0)
b_non_work_mom_sib_bike = Beta('b_non_work_mom_sib_bike', 0, None, None, 0)
b_non_work_dad_sib_bike = Beta('b_non_work_dad_sib_bike', 0, None, None, 0)

b_age_sib_bike = Beta('b_age_sib_bike', 0, None, None, 0)
b_female_sib_bike = Beta('b_female_sib_bike', 0, None, None, 0)
b_has_lil_sib_sib_bike = Beta('b_has_lil_sib_sib_bike', 0, None, None, 0)
b_has_big_sib_sib_bike = Beta('b_has_big_sib_sib_bike', 0, None, None, 0)

b_log_density_sib_bike = Beta('b_log_density_sib_bike', 0, None, None, 0)
b_log_distance_sib_bike = Beta('b_log_distance_sib_bike', 0, None, None, 0)

# Define utility functions
V_mom_car = (
    asc_mom_car +
    b_log_income_k_mom_car * log_income_k +
    b_veh_per_driver_mom_car * veh_per_driver +
    b_non_work_mom_mom_car * non_work_mom +
    b_non_work_dad_mom_car * non_work_dad +
    b_age_mom_car * age +
    b_female_mom_car * female +
    b_has_lil_sib_mom_car * has_lil_sib +
    b_has_big_sib_mom_car * has_big_sib +
    b_log_density_mom_car * log_density +
    b_log_distance_mom_car * log_distance
)

V_MomDad_car = (
    asc_MomDad_car +
    b_log_income_k_MomDad_car * log_income_k +
    b_veh_per_driver_MomDad_car * veh_per_driver +
    b_non_work_mom_MomDad_car * non_work_mom +
    b_non_work_dad_MomDad_car * non_work_dad +
    b_age_MomDad_car * age +
    b_female_MomDad_car * female +
    b_has_lil_sib_MomDad_car * has_lil_sib +
    b_has_big_sib_MomDad_car * has_big_sib +
    b_log_density_MomDad_car * log_density +
    b_log_distance_MomDad_car * log_distance
)

V_dad_car = (
    asc_dad_car +
    b_log_income_k_dad_car * log_income_k +
    b_veh_per_driver_dad_car * veh_per_driver +
    b_non_work_mom_dad_car * non_work_mom +
    b_non_work_dad_dad_car * non_work_dad +
    b_age_dad_car * age +
    b_female_dad_car * female +
    b_has_lil_sib_dad_car * has_lil_sib +
    b_has_big_sib_dad_car * has_big_sib +
    b_log_density_dad_car * log_density +
    b_log_distance_dad_car * log_distance
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

V_sib_car = (
    asc_sib_car +
    b_log_income_k_sib_car * log_income_k +
    b_veh_per_driver_sib_car * veh_per_driver +
    b_non_work_mom_sib_car * non_work_mom +
    b_non_work_dad_sib_car * non_work_dad +
    b_age_sib_car * age +
    b_female_sib_car * female +
    b_has_lil_sib_sib_car * has_lil_sib +
    b_has_big_sib_sib_car * has_big_sib +
    b_log_density_sib_car * log_density +
    b_log_distance_sib_car * log_distance
)

V_mom_walk = (
    asc_mom_walk +
    b_log_income_k_mom_walk * log_income_k +
    b_veh_per_driver_mom_walk * veh_per_driver +
    b_non_work_mom_mom_walk * non_work_mom +
    b_non_work_dad_mom_walk * non_work_dad +
    b_age_mom_walk * age +
    b_female_mom_walk * female +
    b_has_lil_sib_mom_walk * has_lil_sib +
    b_has_big_sib_mom_walk * has_big_sib +
    b_log_density_mom_walk * log_density +
    b_log_distance_mom_walk * log_distance
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

V_MomDad_walk = (
    asc_MomDad_walk +
    b_log_income_k_MomDad_walk * log_income_k +
    b_veh_per_driver_MomDad_walk * veh_per_driver +
    b_non_work_mom_MomDad_walk * non_work_mom +
    b_non_work_dad_MomDad_walk * non_work_dad +
    b_age_MomDad_walk * age +
    b_female_MomDad_walk * female +
    b_has_lil_sib_MomDad_walk * has_lil_sib +
    b_has_big_sib_MomDad_walk * has_big_sib +
    b_log_density_MomDad_walk * log_density +
    b_log_distance_MomDad_walk * log_distance
)

V_dad_walk = (
    asc_dad_walk +
    b_log_income_k_dad_walk * log_income_k +
    b_veh_per_driver_dad_walk * veh_per_driver +
    b_non_work_mom_dad_walk * non_work_mom +
    b_non_work_dad_dad_walk * non_work_dad +
    b_age_dad_walk * age +
    b_female_dad_walk * female +
    b_has_lil_sib_dad_walk * has_lil_sib +
    b_has_big_sib_dad_walk * has_big_sib +
    b_log_density_dad_walk * log_density +
    b_log_distance_dad_walk * log_distance
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

V_sib_walk = (
    asc_sib_walk +
    b_log_income_k_sib_walk * log_income_k +
    b_veh_per_driver_sib_walk * veh_per_driver +
    b_non_work_mom_sib_walk * non_work_mom +
    b_non_work_dad_sib_walk * non_work_dad +
    b_age_sib_walk * age +
    b_female_sib_walk * female +
    b_has_lil_sib_sib_walk * has_lil_sib +
    b_has_big_sib_sib_walk * has_big_sib +
    b_log_density_sib_walk * log_density +
    b_log_distance_sib_walk * log_distance
)

V_mom_bike = (
    asc_mom_bike +
    b_log_income_k_mom_bike * log_income_k +
    b_veh_per_driver_mom_bike * veh_per_driver +
    b_non_work_mom_mom_bike * non_work_mom +
    b_non_work_dad_mom_bike * non_work_dad +
    b_age_mom_bike * age +
    b_female_mom_bike * female +
    b_has_lil_sib_mom_bike * has_lil_sib +
    b_has_big_sib_mom_bike * has_big_sib +
    b_log_density_mom_bike * log_density +
    b_log_distance_mom_bike * log_distance
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

V_MomDad_bike = (
    asc_MomDad_bike +
    b_log_income_k_MomDad_bike * log_income_k +
    b_veh_per_driver_MomDad_bike * veh_per_driver +
    b_non_work_mom_MomDad_bike * non_work_mom +
    b_non_work_dad_MomDad_bike * non_work_dad +
    b_age_MomDad_bike * age +
    b_female_MomDad_bike * female +
    b_has_lil_sib_MomDad_bike * has_lil_sib +
    b_has_big_sib_MomDad_bike * has_big_sib +
    b_log_density_MomDad_bike * log_density +
    b_log_distance_MomDad_bike * log_distance
)

V_dad_bike = (
    asc_dad_bike +
    b_log_income_k_dad_bike * log_income_k +
    b_veh_per_driver_dad_bike * veh_per_driver +
    b_non_work_mom_dad_bike * non_work_mom +
    b_non_work_dad_dad_bike * non_work_dad +
    b_age_dad_bike * age +
    b_female_dad_bike * female +
    b_has_lil_sib_dad_bike * has_lil_sib +
    b_has_big_sib_dad_bike * has_big_sib +
    b_log_density_dad_bike * log_density +
    b_log_distance_dad_bike * log_distance
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

V_sib_bike = (
    asc_sib_bike +
    b_log_income_k_sib_bike * log_income_k +
    b_veh_per_driver_sib_bike * veh_per_driver +
    b_non_work_mom_sib_bike * non_work_mom +
    b_non_work_dad_sib_bike * non_work_dad +
    b_age_sib_bike * age +
    b_female_sib_bike * female +
    b_has_lil_sib_sib_bike * has_lil_sib +
    b_has_big_sib_sib_bike * has_big_sib +
    b_log_density_sib_bike * log_density +
    b_log_distance_sib_bike * log_distance
)

# Associate utility functions with alternative numbers
V = {721: V_MomDad_car,
     722: V_mom_car,
     723: V_dad_car,
     724: V_non_hh_car,
     730: V_sib_car,
     810: V_alone_walk,
     821: V_MomDad_walk,
     822: V_mom_walk,
     823: V_dad_walk,
     824: V_non_hh_walk,
     830: V_sib_walk,
     910: V_alone_bike,
     921: V_MomDad_bike,
     922: V_mom_bike,
     923: V_dad_bike,
     924: V_non_hh_bike,
     930: V_sib_bike}

# Associate availability variables with alternatives
av = {721: with_mom_dad_avail,
      722: with_mom_avail,
      723: with_dad_avail,
      724: with_non_hh_avail,
      730: with_sib_avail,
      810: alone_avail,
      821: with_mom_dad_avail,
      822: with_mom_avail,
      823: with_dad_avail,
      824: with_non_hh_avail,
      830: with_sib_avail,
      910: alone_avail,
      921: with_mom_dad_avail,
      922: with_mom_avail,
      923: with_dad_avail,
      924: with_non_hh_avail,
      930: with_sib_avail}

# Define the model
mode_ind_model = models.loglogit(V, av, mode_ind)

# Create Biogeme object for estimation
mode_ind_biogeme_est = bio.BIOGEME(database_est, mode_ind_model)
mode_ind_biogeme_est.modelName = 'mode_ind_model_est'

# Calculate null log likelihood for reporting
mode_ind_biogeme_est.calculateNullLoglikelihood(av)

# Estimate parameters
results = mode_ind_biogeme_est.estimate()
print(results.shortSummary())

# Get results in a pandas table
pandas_results = results.getEstimatedParameters()
print(pandas_results)

# Save parameters to csv
pandas_results.to_csv('biogeme_parameters_mode_ind.csv')

# Generate predictions
prob_mom_dad_car = models.logit(V, av, 721)
prob_mom_car = models.logit(V, av, 722)
prob_dad_car = models.logit(V, av, 723)
prob_non_hh_car = models.logit(V, av, 724)
prob_sib_car = models.logit(V, av, 730)

prob_alone_walk = models.logit(V, av, 810)
prob_mom_dad_walk = models.logit(V, av, 821)
prob_mom_walk = models.logit(V, av, 822)
prob_dad_walk = models.logit(V, av, 823)
prob_non_hh_walk = models.logit(V, av, 824)
prob_sib_walk = models.logit(V, av, 830)

prob_alone_bike = models.logit(V, av, 910)
prob_mom_dad_bike = models.logit(V, av, 921)
prob_mom_bike = models.logit(V, av, 922)
prob_dad_bike = models.logit(V, av, 923)
prob_non_hh_bike = models.logit(V, av, 924)
prob_sib_bike = models.logit(V, av, 930)

simulate = {'Prob. mom and dad car': prob_mom_dad_car,
            'Prob. mom car': prob_mom_car,
            'Prob. dad car': prob_dad_car,
            'Prob. non-hh car': prob_non_hh_car,
            'Prob. sibling car': prob_sib_car,
            'Prob. alone walk': prob_alone_walk,
            'Prob. mom and dad walk': prob_mom_dad_walk,
            'Prob. mom walk': prob_mom_walk,
            'Prob. dad walk': prob_dad_walk,
            'Prob. non-hh walk': prob_non_hh_walk,
            'Prob. sibling walk': prob_sib_walk,
            'Prob. alone bike': prob_alone_bike,
            'Prob. mom and dad bike': prob_mom_dad_bike,
            'Prob. mom bike': prob_mom_bike,
            'Prob. dad bike': prob_dad_bike,
            'Prob. non-hh bike': prob_non_hh_bike,
            'Prob. sibling bike': prob_sib_bike}

# Create biogeme object for simulation
mode_ind_biogeme_sim = bio.BIOGEME(database_sim, simulate)
mode_ind_biogeme_sim.modelName = "predictions"

betaValues = results.getBetaValues ()
simulatedValues = mode_ind_biogeme_sim.simulate(betaValues)

simulatedValues.to_csv('biogeme_preds_mode_ind.csv')

mom_car_prob_summary = simulatedValues[["Prob. mom car"]].describe()

## 99% probability of mom in all cases?
print(mom_car_prob_summary)