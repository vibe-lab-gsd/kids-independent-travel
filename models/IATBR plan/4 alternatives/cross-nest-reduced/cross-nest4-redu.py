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
df_est = pd.read_csv(here('models/IATBR plan/trips_sc3.csv'))

# Set up biogeme databases
database_est = db.Database('est', df_est)

# Define variables for biogeme
mode_ind = Variable('mode_ind')
veh_per_driver = Variable('sc3_veh_per_driver')
non_work_mom = Variable('sc3_non_work_mom')
non_work_dad = Variable('sc3_non_work_dad')
age = Variable('sc3_age')
female = Variable('sc3_female')
has_lil_sib = Variable('sc3_has_lil_sib')
has_big_sib = Variable('sc3_has_big_sib')
log_income_k = Variable('sc3_log_inc_k')
log_distance = Variable('log_distance')
log_density = Variable('sc3_log_density')
y2017 = Variable('sc3_y2017')
av_par_car = Variable('av_par_car')
av_par_act = Variable('av_par_act')
av_kid_car = Variable('av_kid_car')
av_kid_act = Variable('av_kid_act')

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
b_log_density_par_car = Beta('b_log_density_par_car', 0, None, None, 1)
b_y2017_par_car = Beta('b_y2017_par_car', 0, None, None, 1)

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
b_log_density_par_act = Beta('b_log_density_par_act', 0, None, None, 0)
b_y2017_par_act = Beta('b_y2017_par_act', 0, None, None, 0)

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
b_log_density_kid_car = Beta('b_log_density_kid_car', 0, None, None, 0)
b_y2017_kid_car = Beta('b_y2017_kid_car', 0, None, None, 0)

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
b_log_density_kid_act = Beta('b_log_density_kid_act', 0, None, None, 0)
b_y2017_kid_act = Beta('b_y2017_kid_act', 0, None, None, 0)

# MU parameters for nests
mu_parent = Beta('mu_parent', 1, 1, None, 0)
mu_no_parent = Beta('mu_no_parent', 1, 1, None, 0)
mu_motor = Beta('mu_motor', 1, 1, None, 0)
mu_active = Beta('mu_active', 1, 1, None, 0)

# nest membership parameters
alpha_kid_CAR = Beta('alpha_kid_CAR', 0.5, 0, 1, 0)
alpha_KID_car = 1 - alpha_kid_CAR

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
    b_log_distance_par_car * log_distance +
    b_log_density_par_car * log_density +
    b_y2017_par_car * y2017
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
    b_log_distance_par_act * log_distance +
    b_log_density_par_act * log_density +
    b_y2017_par_act * y2017
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
    b_log_distance_kid_car * log_distance +
    b_log_density_kid_car * log_density +
    b_y2017_kid_car * y2017
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
    b_log_distance_kid_act * log_distance +
    b_log_density_kid_act * log_density +
    b_y2017_kid_act * y2017
)

# Associate utility functions with alternative numbers
V = {17: V_par_car,
     18: V_par_act,
     27: V_kid_car,
     28: V_kid_act}

# associate availability conditions with alternatives:

av = {17: av_par_car,
      18: av_par_act,
      27: av_kid_car,
      28: av_kid_act}

# Definition of nests

kid_nest = OneNestForCrossNestedLogit(
    nest_param=mu_no_parent,
    dict_of_alpha={27: alpha_KID_car,
                   28: 1},
    name='kid'
)

motor_nest = OneNestForCrossNestedLogit(
    nest_param=mu_motor,
    dict_of_alpha={17: 1,
                   27: alpha_kid_CAR},
    name='motor'
)

nests = NestsForCrossNestedLogit(
    choice_set=[17, 18, 27, 28],
    tuple_of_nests=(kid_nest,
                    motor_nest)
)

# Define model1
cross_nest = models.logcnl(V, av, nests, mode_ind)

# Create biogeme object
the_biogeme = bio.BIOGEME(database_est, cross_nest)
the_biogeme.modelName = 'cross_nest'

# estimate parameters
results = the_biogeme.estimate()

print(results.short_summary())