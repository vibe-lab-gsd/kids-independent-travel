# Data Assembly notes

## Sample

Data are drawn from the 2017 National Household Travel Survey
(https://nhts.ornl.gov/).

### Criteria for inclusion in sample

* Trip distance is shorter than 2km/1.25 miles
* Trip ends at school
* Traveler is between 8 and 13
* Trip is not by transit, motorcycle, or an unspecified mode (these are rare,
and I assume they are not available to the remaining children)
* Child does not use a school bus for the trip to _or_ from school (assume
the remaining students are ineligible for school bus service)
* Survey does not indicate that the child drove to school unaccompanied (assume 
these are survey coding errors)
* Survey does not indicate the child traveled to school by car with
only siblings unless the child has a sibling who is a driver.
* Data not missing for any outcome or predictor variables
* To filter out some weird cases and only have one trip per child:
    * Trip does not begin AND end at school
    * Trip ends before 10am
    * This is the first qualifying trip of the day

### Multi-stage trips

If the trip ending at school begins with a transfer from another
mode, the prior trip is included as part of this trip, and trip
characteristics are determined as follows:

* Match the characteristics of the longest-distance segment of the trip
    * Mode
    * Presence of others
* Summed across all segments
    * Trip distance
* Taken from the first segment of the trip
    * Population density at trip origin
    * All individual- and household-level variables
* Taken from last segment of trip
    * Population density at trip destination

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

### Predictor variables

* Household-level variables
    * income_k: NHTS codes income in one of 11 income categories. We
convert this to a continuous variable by assigning households in each
category the mid-point value of that category. The highest income category
is for incomes greater than $200,000 per year. We assign an income of
$250,000 to that category. 
    * veh_per_driver: We divide the number of household vehicles by the
number of household drivers. We assign a value of zero to households with
zero drivers
    * n_adults: The number of household adults
    * has_mom: A binary variable indicating whether there is a female
adult in the household
    * has_dad: A binary variable indicating whether there is a male
adult in the household
    * non_work_mom: A binary variable indicating whether there is a female
adult in the household who is not a worker
    * non_work_dad: A binary variable indicating whether there is a male
adult in the household who is not a worker
Individual-level variables
    * age: The child's age
    * female: A binary variable indicating whether the child is female
    * has_lil_sib: A binary variable indicating whether there are any
younger children in the household
    * has_big_sib: A binary variable indicating whether there are any
older children in the household
Trip-level variables
    * distance: Trip distance in kilometers. The NHTS records distance
in miles and these are converted to kilometers by multiplying by 1.609.
    * density: The approximate population density of the census block
in which the trip begins or ends (whichever is higher). NHTS reports
this value in people per square mile. We convert to people per square
kilometer by dividing by 2.59.

## Summary statistics

### Outcomes

Table: Number of trips in sample by mode and (full) independence

|-                  |  Car| Bike| Walk| Total|
|:------------------|----:|----:|----:|-----:|
|Alone              |    0|   67|  155|   222|
|With mom and dad   |   21|    2|   11|    34|
|With mom           |  670|   16|  115|   801|
|With dad           |  308|    6|   46|   360|
|With non-household |   58|    8|   68|   134|
|With siblings      |    7|   15|   85|   107|
|Total              | 1064|  114|  480|  1658|

Table: Share of trips in sample by mode and (full) independence

|-                  |Car   |Bike |Walk |Total |
|:------------------|:-----|:----|:----|:-----|
|Alone              |0%    |4%   |9.3% |13.4% |
|With mom and dad   |1.3%  |0.1% |0.7% |2.1%  |
|With mom           |40.4% |1%   |6.9% |48.3% |
|With dad           |18.6% |0.4% |2.8% |21.7% |
|With non-household |3.5%  |0.5% |4.1% |8.1%  |
|With siblings      |0.4%  |0.9% |5.1% |6.5%  |
|Total              |64.2% |6.9% |29%  |100%  |

Table: Number of trips in sample by mode and (simplified) independence

|-           |  Car| Bike| Walk| Total|
|:-----------|----:|----:|----:|-----:|
|Alone       |    0|   67|  155|   222|
|With adults | 1057|   32|  240|  1329|
|With kids   |    7|   15|   85|   107|
|Total       | 1064|  114|  480|  1658|

Table: Share of trips in sample by mode and (simplified) independence

|-           |Car   |Bike |Walk  |Total |
|:-----------|:-----|:----|:-----|:-----|
|Alone       |0%    |4%   |9.3%  |13.4% |
|With adults |63.8% |1.9% |14.5% |80.2% |
|With kids   |0.4%  |0.9% |5.1%  |6.5%  |
|Total       |64.2% |6.9% |29%   |100%  |

Table: Number of trips in sample by mode and (alternative simplified) independence

|-           |  Car| Bike| Walk| Total|
|:-----------|----:|----:|----:|-----:|
|Alone       |    0|   67|  155|   222|
|With adults |  999|   24|  172|  1195|
|With kids   |   65|   23|  153|   241|
|Total       | 1064|  114|  480|  1658|

Table: Share of trips in sample by mode and (alternative simplified) independence

|-           |Car   |Bike |Walk  |Total |
|:-----------|:-----|:----|:-----|:-----|
|Alone       |0%    |4%   |9.3%  |13.4% |
|With adults |60.3% |1.4% |10.4% |72.1% |
|With kids   |3.9%  |1.4% |9.2%  |14.5% |
|Total       |64.2% |6.9% |29%   |100%  |

### Predictors

Table: Descriptive statistics of predictor variables

|Predictor      |     Mean| Standard Deviation|
|:--------------|--------:|------------------:|
|age            |   10.158|              1.644|
|density        | 2482.977|           2256.667|
|distance       |    1.099|              0.485|
|female         |    0.479|                 NA|
|has_big_sib    |    0.457|                 NA|
|has_dad        |    0.858|                 NA|
|has_lil_sib    |    0.393|                 NA|
|has_mom        |    0.967|                 NA|
|income_k       |   97.603|             70.048|
|n_adults       |    2.044|              0.696|
|non_work_dad   |    0.110|                 NA|
|non_work_mom   |    0.345|                 NA|
|veh_per_driver |    1.090|              0.510|
