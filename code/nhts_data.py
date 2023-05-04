"""" File nhts_data.py

This is where I'll take a first try at setting up a discrete choice model
predicting mode and independence for the journey to school.

See https://github.com/urban-stack/kids-independent-travel for full context
"""

import pandas as pd
import biogeme.database as db
from biogeme.expressions import Variable

df = pd.read_csv('data/usa-2017.dat', sep = '\t')
database = db.Database('trips', df)

mode = Variable('mode')
veh_per_driver = Variable('veh_per_driver')
n_adults = Variable('n_adults')
non_work_mom = Variable('non_work_mom')
non_work_dad = Variable('non_work_dad')
age = Variable('age')
female = Variable('female')
has_lil_sib = Variable('has_lil_sib')
has_big_sib = Variable('has_big_sib')
log_inc_k = Variable('log_income_k')
log_distance = Variable('log_distance')
log_density = Variable('log_density')
av_car = Variable('av_car')
av_walk = Variable('av_walk')
av_bike = Variable('av_bike')


