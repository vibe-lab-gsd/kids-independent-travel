# Example: https://github.com/michelbierlaire/biogeme/blob/master/examples/swissmetro/b11cnl.py
# Cross-nested model to see where non-household companions fit.

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

mu_hh_adult = Beta('mu_hh_adult', )