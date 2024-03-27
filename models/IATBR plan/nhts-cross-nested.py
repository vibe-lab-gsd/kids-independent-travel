# Cross-nested model


import pandas as pd

import biogeme.biogeme as bio
from biogeme import models
from biogeme.expressions import Beta
import biogeme.database as db
from biogeme.expressions import Variable
from biogeme.nests import OneNestForCrossNestedLogit, NestsForCrossNestedLogit

from pyprojroot.here import here

# Read in data
df_est = pd.read_csv(here('models/IATBR plan/trips.csv'))

# Set up biogeme databases
database_est = db.Database('est', df_est)

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
av_motor = Variable('av_motor')
av_active = Variable('av_active')
av_with_parent = Variable('av_with_parent')
av_no_parent = Variable('av_no_parent')

# alternative specific constants (car with parent is reference case)
asc_par_car = Beta('asc_par_car', 0, None, None, 1)
asc_par_act = Beta('asc_par_act', 0, None, None, 0)
asc_kid_car = Beta('asc_kid_car', 0, None, None, 0)
asc_kid_act = Beta('asc_kid_act', 0, None, None, 0)

# parent car betas (not estimated for reference case)
b_log_income_k_par_car = Beta('b_log_income_k_par_car', 0, None, None, 1)
b_veh_per_driver_par_car = Beta('b_veh_per_driver_par_car', 0, None, None, 1)
b_non_work_mom_par_car = Beta('b_non_work_mom_par_car', 0, None, None, 1)
b_non_work_dad_par_car = Beta('b_non_work_dad_par_car', 0, None, None, 1)

b_age_par_car = Beta('b_age_par_car', 0, None, None, 1)
b_female_par_car = Beta('b_female_par_car', 0, None, None, 1)
b_has_lil_sib_par_car = Beta('b_has_lil_sib_par_car', 0, None, None, 1)
b_has_big_sib_par_car = Beta('b_has_big_sib_par_car', 0, None, None, 1)

b_log_distance_par_car = Beta('b_log_distance_par_car', 0, None, None, 1)

# betas for with parent active
b_log_income_k_par_act = Beta('b_log_income_k_par_act', 0, None, None, 0)
b_veh_per_driver_par_act = Beta('b_veh_per_driver_par_act', 0, None, None, 0)
b_non_work_mom_par_act = Beta('b_non_work_mom_par_act', 0, None, None, 0)
b_non_work_dad_par_act = Beta('b_non_work_dad_par_act', 0, None, None, 0)

b_age_par_act = Beta('b_age_par_act', 0, None, None, 0)
b_female_par_act = Beta('b_female_par_act', 0, None, None, 0)
b_has_lil_sib_par_act = Beta('b_has_lil_sib_par_act', 0, None, None, 0)
b_has_big_sib_par_act = Beta('b_has_big_sib_par_act', 0, None, None, 0)

b_log_distance_par_act = Beta('b_log_distance_par_act', 0, None, None, 0)

# betas for with kid car
b_log_income_k_kid_car = Beta('b_log_income_k_kid_car', 0, None, None, 0)
b_veh_per_driver_kid_car = Beta('b_veh_per_driver_kid_car', 0, None, None, 0)
b_non_work_mom_kid_car = Beta('b_non_work_mom_kid_car', 0, None, None, 0)
b_non_work_dad_kid_car = Beta('b_non_work_dad_kid_car', 0, None, None, 0)

b_age_kid_car = Beta('b_age_kid_car', 0, None, None, 0)
b_female_kid_car = Beta('b_female_kid_car', 0, None, None, 0)
b_has_lil_sib_kid_car = Beta('b_has_lil_sib_kid_car', 0, None, None, 0)
b_has_big_sib_kid_car = Beta('b_has_big_sib_kid_car', 0, None, None, 0)

b_log_distance_kid_car = Beta('b_log_distance_kid_car', 0, None, None, 0)

# betas for kid active
b_log_income_k_kid_act = Beta('b_log_income_k_kid_act', 0, None, None, 0)
b_veh_per_driver_kid_act = Beta('b_veh_per_driver_kid_act', 0, None, None, 0)
b_non_work_mom_kid_act = Beta('b_non_work_mom_kid_act', 0, None, None, 0)
b_non_work_dad_kid_act = Beta('b_non_work_dad_kid_ace', 0, None, None, 0)

b_age_kid_act = Beta('b_age_kid_act', 0, None, None, 0)
b_female_kid_act = Beta('b_female_kid_act', 0, None, None, 0)
b_has_lil_sib_kid_act = Beta('b_has_lil_sib_kid_act', 0, None, None, 0)
b_has_big_sib_kid_act = Beta('b_has_big_sib_kid_act', 0, None, None, 0)

b_log_distance_kid_act = Beta('b_log_distance_kid_act', 0, None, None, 0)

# MU parameters for nests
mu_parent = Beta('mu_parent', 1, 1, 100, 0)
mu_no_parent = Beta('mu_no_parent', 1, 1, 100, 0)
mu_motor = Beta('mu_motor', 1, 1, 100, 0)
mu_active = Beta('mu_active', 1, 1, 100, 0)

# nest membership parameters
alpha_par_CAR = Beta('alpha_par_CAR', 0.5, 0, 1, 0)
alpha_PAR_car = 1 - alpha_par_CAR

alpha_kid_CAR = Beta('alpha_kid_CAR', 0.5, 0, 1, 0)
alpha_KID_car = 1 - alpha_kid_CAR

alpha_par_ACT = Beta('alpha_par_ACT', 0.5, 0, 1, 0)
alpha_PAR_act = 1 - alpha_par_ACT

alpha_kid_ACT = Beta('alpha_kid_ACT', 0.5, 0, 1, 0)
alpha_KID_act = 1 - alpha_kid_ACT

# Definition of utility functions
V_par_car = (
    asc_par_car +
    b_log_income_k_par_car * log_income_k +
    b_veh_per_driver_par_car * veh_per_driver +
    b_non_work_mom_par_car * non_work_mom +
    b_non_work_dad_par_car * non_work_dad +
    b_age_par_car * age +
    b_female_par_car * female +
    b_has_lil_sib_par_car * has_lil_sib +
    b_has_big_sib_par_car * has_big_sib +
    b_log_distance_par_car * log_distance
)

V_par_act = (
    asc_par_act +
    b_log_income_k_par_act * log_income_k +
    b_veh_per_driver_par_act * veh_per_driver +
    b_non_work_mom_par_act * non_work_mom +
    b_non_work_dad_par_act * non_work_dad +
    b_age_par_act * age +
    b_female_par_act * female +
    b_has_lil_sib_par_act * has_lil_sib +
    b_has_big_sib_par_act * has_big_sib +
    b_log_distance_par_act * log_distance
)

V_kid_car = (
    asc_kid_car +
    b_log_income_k_kid_car * log_income_k +
    b_veh_per_driver_kid_car * veh_per_driver +
    b_non_work_mom_kid_car * non_work_mom +
    b_non_work_dad_kid_car * non_work_dad +
    b_age_kid_car * age +
    b_female_kid_car * female +
    b_has_lil_sib_kid_car * has_lil_sib +
    b_has_big_sib_kid_car * has_big_sib +
    b_log_distance_kid_car * log_distance
)

V_kid_act = (
    asc_kid_act +
    b_log_income_k_kid_act * log_income_k +
    b_veh_per_driver_kid_act * veh_per_driver +
    b_non_work_mom_kid_act * non_work_mom +
    b_non_work_dad_kid_act * non_work_dad +
    b_age_kid_act * age +
    b_female_kid_act * female +
    b_has_lil_sib_kid_act * has_lil_sib +
    b_has_big_sib_kid_act * has_big_sib +
    b_log_distance_kid_act * log_distance
)

# Associate utility functions with alternative numbers
V = {17: V_par_car,
     18: V_par_act,
     27: V_kid_car,
     28: V_kid_act}

# associate availability conditions with alternatives:
# Note: the names don't really make sense with what we're doing,
# but they're all 1s - all alternatives are available to everyone

av = {17: av_motor,
      18: av_active,
      27: av_with_parent,
      28: av_no_parent}

# Definition of nests
par_nest = OneNestForCrossNestedLogit(
    nest_param=mu_parent,
    dict_of_alpha={17: alpha_PAR_car,
                   18: alpha_PAR_act},
    name='parent'
)

kid_nest = OneNestForCrossNestedLogit(
    nest_param=mu_no_parent,
    dict_of_alpha={27: alpha_KID_car,
                   28: alpha_KID_act},
    name='kid'
)

active_nest = OneNestForCrossNestedLogit(
    nest_param=mu_active,
    dict_of_alpha={18: alpha_par_ACT,
                   28: alpha_kid_ACT},
    name='active'
)

motor_nest = OneNestForCrossNestedLogit(
    nest_param=mu_motor,
    dict_of_alpha={17: alpha_par_CAR,
                   27: alpha_kid_CAR},
    name='motor'
)

nests = NestsForCrossNestedLogit(
    choice_set=[17, 18, 27, 28],
    tuple_of_nests=(par_nest,
                    kid_nest,
                    active_nest,
                    motor_nest)
)

# Define model
cross_nest = models.logcnl(V, av, nests, mode_ind)

# Create biogeme object
the_biogeme = bio.BIOGEME(database_est, cross_nest)
the_biogeme.modelName = 'cross_nest'

# estimate parameters
results = the_biogeme.estimate()

print(results.short_summary())