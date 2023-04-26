# Data Assembly notes

## Criteria for inclusion in initial sample

* Trip distance is (not missing and) shorter than 2km/1.25 miles
* Trip ends at school
* Traveler is older between 8 and 13
* To filter out some weird cases:
    * Trip does not begin AND end at school
    * Trip ends before 10am
    * This is the first qualifying trip of the day

# Multi-stage trips
If the trip ending at school begins with a transfer from another
mode, the prior trip is included as part of this trip, and trip
characteristics are determined as follows:

* Match the characteristics of the longest-distance segment of the trip
    * Mode
    * Presence of others
* Summed across all segments
    * Trip distnace
* Taken from the first segment of the trip
    * Population density at trip origin
    * All individual- and houshold-level variables
* Taken from last segment of trip
    * Population density at trip destination

Table: Initial sample

|Type                 | Sample size|
|:--------------------|-----------:|
|Number of trips      |        2165|
|Number of children   |        2165|
|Number of households |        1758|

Table: Trips by mode in initial sample

|mode        | Trips in sample|
|:-----------|---------------:|
|bike        |             119|
|car         |            1228|
|motorcycle  |               2|
|school bus  |             286|
|transit     |              10|
|unspecified |              11|
|walk        |             509|
