"""" File build-model.py

This is where I'll take a first try at setting up a discrete choice model
predicting mode and independence for the journey to school.

See https://github.com/urban-stack/kids-independent-travel for full context
"""

import biogeme.database as db
import pandas as pd

# Read the data
df = pd.read_csv('data/usa-2017.dat', sep='\t')
database = db.Database('school_trips', df)

#  save a file