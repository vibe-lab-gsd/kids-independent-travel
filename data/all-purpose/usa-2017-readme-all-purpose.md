# Data Assembly notes

## Sample

Data are drawn from the 2017 National Household Travel Survey
(https://nhts.ornl.gov/).

### Criteria for inclusion in sample

* Trip distance is shorter than 2km/1.25 miles
* Traveler is between 8 and 13
* School trips are excluded for children who used a school bus on the
travel day
* Survey does not indicate that the child drove unaccompanied (assume 
these are survey coding errors)
* Survey does not indicate the child traveled by car with
only siblings unless the child has a sibling who is a driver.
* Data not missing for any outcome or predictor variables
* Trips with the purpose of transfering to another mode are included
as separate trips.

## Variables

### Outcome variables
* 'mode': One of
    * 7 = car
    * 8 = walk
    * 9 = bike
* 'independence': (string) For purposes of this analysis, we describe all
female household adults as moms, all male household adults as dads, and all
household children as siblings. Also note that NHTS codes all household
members as either male or female. We know how many non-household members
are on a trip, but we don't know their ages, genders, or drivers status.
The full independence variable takes one
of the following 6 values to describe who was with the child on their trip
to school:
    * 10 = alone: There was only one person (the child) on the trip.
    * 21 = with mom and dad: The child was accompanied by a male household adult
_and_ a female household adult.
    * 22 = with mom: The child was accompanied by a female household adult
but no male household adult.
    * 23 = with dad: The child was accompanied by a male household adult but
no female household adult.
no household adults or non-household members.
    * 24 = with non-household: The child was accompanied by non-household
members and no household members were on the trip.
    * 30 = with sibling: The child was accompanied by household children, but
* 'ind_3': A simplified independence variable. One of:
    * 10 = alone: Same as 1 (alone) in the full independence variable
    * 20 = with adults: Combination of these values from the full
independence variable:
        * 21 (with mom and dad)
        * 22 (with mom)
        * 23 (with dad)
        * 24 (with non-household)
    * 30 = with kids: same as 3 (with sibling) in the full independence variable.
* 'ind_3_alt': Same as 'ind_3a', but trips with non-household members
(indpendence = 3) are classified as trips with kids. Since we don't know if the
non-household members are kids or adults, we might want to test it both
ways and see if it effects the result.
* 'mode_ind': Combination of mode and the full independence variable. Takes
the following values:
    * 721 = car with mom and dad
    * 722 = car with mom
    * 723 = car with dad
    * 724 = car with non-household
    * 730 = car with sibling
    * 810 = walk alone
    * 821 = walk with mom and dad
    * 822 = walk with mom
    * 823 = walk with dad
    * 824 = walk with non-household
    * 830 = walk with sibling
    * 910 = bike alone
    * 921 = bike with mom and dad
    * 922 = bike with mom
    * 923 = bike with dad
    * 924 = bike with non-household
    * 930 = bike with sibling
* 'mode_ind_3': Combination of mode and the simplified independence
variable. Takes the following values
    *720 = car with adult
    *730 = car with kid
    *810 = walk alone
    *820 = walk with adults
    *830 = walk with kids
    *910 = bike alone
    *920 = bike with adults
    *930 = bike with kids
* 'mode_ind_3_alt': Combination of mode and the simplified independence
variable that classifies non-household members as kids. Same categories
as 'mode_ind_3.

### Availability variables

'av_car', 'av_walk', and 'av_bike' indicate the trips for which travel by
car, walking, or bike is available. We are assuming that these three modes
are available for all children in the sample (even if there is not car in
the household, since some children in the sample in zero-vehicle households
_do_ travel by car) so this value is set to one for all cases.

The following variables indicate the availability of independence
alternatives:

* alone_avail: TRUE/1 for all trips
* with_mom_dad_avail: True if there is both a female and a male adult in
the household.
* with_mom_avail: True if there is a female adult in the household
* with_dad_avail: True if there is a male adult in the household
* with_non_hh_avail: True for all trips
* with_sib_avail: True if there are any other children in the household
* with_adult_avail: True for all trips

### Predictor variables

* Household-level variables
    * income_k: NHTS codes income in one of 11 income categories. We
convert this to a continuous variable by assigning households in each
category the mid-point value of that category. The highest income category
is for incomes greater than $200,000 per year. We assign an income of
$250,000 to that category. log_income_k is the natural log of income_k.
    * veh_per_driver: We divide the number of household vehicles by the
number of household drivers. We assign a value of zero to households with
zero drivers
    * n_adults: The number of household adults
    * non_work_mom: A binary variable indicating whether there is a female
adult in the household who is not a worker
    * non_work_dad: A binary variable indicating whether there is a male
adult in the household who is not a worker
* Individual-level variables
    * age: The child's age
    * female: A binary variable indicating whether the child is female
    * has_lil_sib: A binary variable indicating whether there are any
younger children in the household (includes children who are the same
age as the respondent).
    * has_big_sib: A binary variable indicating whether there are any
older children in the household
* Trip-level variables
    * school: A binary variable indicating whether this is a school trip
    * distance: Trip distance in kilometers. The NHTS records distance
in miles and these are converted to kilometers by multiplying by 1.609.
log_distance is the natural log of distance.
    * density: The approximate population density of the census block
in which the trip begins or ends (whichever is higher). NHTS reports
this value in people per square mile. We convert to people per square
kilometer by dividing by 2.59. log_density is the natural log of density.
* Travel-day variables
    * had_school: Child attended school
    * Distance from home to school (km)
    * n_non_school_trips: Number of non-school trips that day
    * avg_trip_dist: Average length of trips that day (km)

Table: Modes excluded from analysis

|Mode                              | Number of trips|
|:---------------------------------|---------------:|
|Golf cart or segway               |              12|
|Moped or motorcycle               |              16|
|RV, motorhome, ATV, or snowmobile |               7|
|Transit                           |              54|
|Unspecified                       |              66|
## Summary statistics

### Outcomes

Table: Number of trips in sample by mode and (full) independence

|-                  |  Car| Bike| Walk| Total|
|:------------------|----:|----:|----:|-----:|
|Alone              |    0|  396| 1197|  1593|
|With mom and dad   |  884|   19|  314|  1217|
|With mom           | 3534|   76|  902|  4512|
|With dad           | 1316|   38|  257|  1611|
|With non-household |  373|  110|  478|   961|
|With siblings      |   30|  114|  604|   748|
|Total              | 6137|  753| 3752| 10684|

Table: Share of trips in sample by mode and (full) independence

|-                  |Car   |Bike |Walk  |Total |
|:------------------|:-----|:----|:-----|:-----|
|Alone              |0%    |3.7% |11.2% |14.9% |
|With mom and dad   |8.3%  |0.2% |2.9%  |11.4% |
|With mom           |33.1% |0.7% |8.4%  |42.2% |
|With dad           |12.3% |0.4% |2.4%  |15.1% |
|With non-household |3.5%  |1%   |4.5%  |9%    |
|With siblings      |0.3%  |1.1% |5.7%  |7%    |
|Total              |57.4% |7%   |35.1% |100%  |

Table: Number of trips in sample by mode and (simplified) independence

|-           |  Car| Bike| Walk| Total|
|:-----------|----:|----:|----:|-----:|
|Alone       |    0|  396| 1197|  1593|
|With adults | 6107|  243| 1951|  8301|
|With kids   |   30|  114|  604|   748|
|Total       | 6137|  753| 3752| 10684|

Table: Share of trips in sample by mode and (simplified) independence

|-           |Car   |Bike |Walk  |Total |
|:-----------|:-----|:----|:-----|:-----|
|Alone       |0%    |3.7% |11.2% |14.9% |
|With adults |57.2% |2.3% |18.3% |77.7% |
|With kids   |0.3%  |1.1% |5.7%  |7%    |
|Total       |57.4% |7%   |35.1% |100%  |

Table: Number of trips in sample by mode and (alternative simplified) independence

|-           |  Car| Bike| Walk| Total|
|:-----------|----:|----:|----:|-----:|
|Alone       |    0|  396| 1197|  1593|
|With adults | 5734|  133| 1473|  7340|
|With kids   |  403|  224| 1082|  1709|
|Total       | 6137|  753| 3752| 10684|

Table: Share of trips in sample by mode and (alternative simplified) independence

|-           |Car   |Bike |Walk  |Total |
|:-----------|:-----|:----|:-----|:-----|
|Alone       |0%    |3.7% |11.2% |14.9% |
|With adults |53.7% |1.2% |13.8% |68.7% |
|With kids   |3.8%  |2.1% |10.1% |16%   |
|Total       |57.4% |7%   |35.1% |100%  |

### Choice availability

Table: Prevalence and availability of full independence choices

|Full independence variable |Percent selected |Percent available |
|:--------------------------|:----------------|:-----------------|
|Alone                      |15%              |100%              |
|With mom and dad           |11%              |82%               |
|With mom                   |42%              |97%               |
|With dad                   |15%              |85%               |
|With non-household         |9%               |100%              |
|With siblings              |7%               |80%               |

### Predictors

Table: Descriptive statistics of predictor variables

|Predictor          |     Mean| Standard Deviation|
|:------------------|--------:|------------------:|
|age                |   10.345|              1.685|
|avg_trip_dist      |    5.225|             15.292|
|density            | 2240.353|           2365.836|
|distance           |    0.959|              0.563|
|female             |    0.488|                 NA|
|had_school         |    0.582|                 NA|
|has_big_sib        |    0.449|                 NA|
|has_lil_sib        |    0.475|                 NA|
|income_k           |   99.215|             71.414|
|n_adults           |    1.991|              0.625|
|n_non_school_trips |    3.295|              2.650|
|non_work_dad       |    0.115|                 NA|
|non_work_mom       |    0.358|                 NA|
|school             |    0.328|                 NA|
|school_dist        |    6.261|             85.676|
|veh_per_driver     |    1.092|              0.498|
