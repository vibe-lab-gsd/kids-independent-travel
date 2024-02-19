# Children's Independent Mobility and Active Travel

The purpose of this project is to study relationships between
children's independent mobility and the use of active modes of 
transportation.

## Project team

Contributors to this project include: 

* Carole Turley Voulgaris (Harvard), with assistance from
    * Aanchal Chopra
    * Sheyla Chevarria
    * Dawon Oh
* Greg Macfarlane (Brigham Young University)
* Anders Fjendbo Jensen (TU Denmark)

## Repository contents

This repository contains the following subfolders:

### data

Contains datasets for analysis. Organized into two subfolders:

* *all-purpose* includes a study sample of trips by children _for all trip purposes_ from
the 2017 National Household travel survey. The same dataset is included as a *.dat
file (for use in the Python/Biogeme models) and as a *.rds file (for use in R/mlogit
models). There is also a readme file that describes the criteria for inclusion in
the sample, describes what each of the variables represents, and shows some
basic descriptive statistics.

* *only-school* includes a study sample of trips _to school_ by children from
the 2017 National Household travel survey. The same dataset (usa-2017) is included as a *.dat
file (for use in the Python/Biogeme models) and as a *.rds file (for use in R/mlogit
models). There is also a readme file that describes the criteria for inclusion in
the sample, describes what each of the variables represents, and shows some
basic descriptive statistics. There is also a pair of files (\*.dat and \*.rds)
with simulated data that vary each variable across a reasonable range while 
holding other variables constant. These are for generating figures with 
predicted probabilities to illustrate model results. 

### data-assembly

These are the scripts that generated the files in the *data* subfolder.

### extra-R-functions

This includes one R script defining some functions that help set up data for 
analysis using the mlogit package.

## lit-review

This is a place to store files related to the literature review. So far, the 
only thing in here is working paper that we submitted to TRB in the summer of 2023.

## Models

Documentation to come.
