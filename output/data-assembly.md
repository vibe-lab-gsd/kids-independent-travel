# Data Assembly notes

## Sample

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
* Data not missing for any independent or dependent variables
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

### Identifiers
* 'trip_person_hh': (string) Unique trip identifier
* 'person_hh': (string) Unique person identifier
* 'HOUSEID': (number) Unique household identifier

### Dependent variables
* 'mode': (string) One of
    * 'car,'
    * 'walk,' or
    * 'bike'
* 'independence': (string) For purposes of this analysis, we describe all
female household adults as moms, all male household adults as dads, and all
household children as siblings. Also note that NHTS codes all household
members as either male or female. We know how many non-household members
are on a trip, but we don't know their ages, genders, or drivers status.
The full independence variable takes one
of the following 6 values to describe who was with the child on their trip
to school:
    * 'alone': There was only one person (the child) on the trip.
    * 'with_mom+dad': The child was accompanied by a male household adult
and a female household adult.
    * 'with_mom': The child was accompanied by a female household adult
but no male household adult.
    * 'with_dad': The child was accompanied by a male household adult but
no female household adult.
    *'with_sibling': The child was accompanied by household children, but
no household adults or non-household members.
    *'others': The child was accompanied by non-household members and no
household members were on the trip.
* 'ind_3a': (string) A simplified independence variable. One of:
    * 'alone': Same as 'alone' in the full independence variable
    * 'with adults': Combination of 'with_mom+dad', 'with_mom',
'with_dad', and 'with_non_hh'.
    * 'with_kids': same as 'with_sibling' in the full independence variable.
* 'ind_3b': (string) Same as 'ind_3a', but the 'with_non_hh' variable is
grouped with the 'with_kids' category. Since we don't know if the
non-household members are kids or adults, we might want to test it both
ways and see if it effects the result.
