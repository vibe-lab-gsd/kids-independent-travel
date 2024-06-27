# Model predicts the choice among four alternatives:
#   * Car with a parent
#   * Car without a parent (presumably a carpool)
#   * Active with a parent
#   * Active without a parent

# In this model, the alternatives are nested by parental escort

import pandas as pd

import biogeme.biogeme as bio
from biogeme import models
from biogeme.expressions import Beta
import biogeme.database as db
from biogeme.expressions import Variable
from biogeme.nests import OneNestForNestedLogit, NestsForNestedLogit

from pyprojroot.here import here

# Read in data
df_est = pd.read_csv(here('models/IATBR plan/trips_sc2.csv'))

# Set up biogeme databases
database_est = db.Database('est', df_est)

# Define variables for biogeme
mode_ind = Variable('mode_ind')
y2017 = Variable('sc2_y2017')
veh_per_driver = Variable('sc2_veh_per_driver')
non_work_mom = Variable('sc2_non_work_mom')
non_work_dad = Variable('sc2_non_work_dad')
age = Variable('sc2_age')
female = Variable('sc2_female')
has_lil_sib = Variable('sc2_has_lil_sib')
has_big_sib = Variable('sc2_has_big_sib')
log_inc_k = Variable('sc2_log_inc_k')
log_distance = Variable('log_distance')
log_density = Variable('sc2_log_density')
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

# Definition of utility functions
V_par_car = (
    asc_par_car +
    b_log_income_k_par_car * log_inc_k +
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
    b_log_income_k_par_act * log_inc_k +
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
    b_log_income_k_kid_car * log_inc_k +
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
    b_log_income_k_kid_act * log_inc_k +
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

# Define nests based on independence
mu_parent = Beta('mu_parent', 1, 1.0, None, 0)
mu_kid = Beta('mu_kid', 1, 1.0, None, 0)

parent_nest = OneNestForNestedLogit(
    nest_param=mu_parent,
    list_of_alternatives=[17,18],
    name='parent_nest'
)

kid_nest = OneNestForNestedLogit(
    nest_param=mu_kid,
    list_of_alternatives=[27,28],
    name='kid_nest'
)

ind_nests = NestsForNestedLogit(
    choice_set=list(V),
    tuple_of_nests=(parent_nest,
                    kid_nest)
)

# Define model
my_model = models.lognested(V, av, ind_nests, mode_ind)

# Create biogeme object
the_biogeme = bio.BIOGEME(database_est, my_model)
the_biogeme.modelName = 'ind_nests'

# estimate parameters
results = the_biogeme.estimate()

print(results.short_summary())