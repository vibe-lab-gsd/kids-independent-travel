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

### Dependent variables
* 'mode': One of
    * 1 = car,
    * 2 = walk,
    * 3 = bike
* 'independence': (string) For purposes of this analysis, we describe all
female household adults as moms, all male household adults as dads, and all
household children as siblings. Also note that NHTS codes all household
members as either male or female. We know how many non-household members
are on a trip, but we don't know their ages, genders, or drivers status.
The full independence variable takes one
of the following 6 values to describe who was with the child on their trip
to school:
    * 1 = alone: There was only one person (the child) on the trip.
    * 21 = with mom and dad: The child was accompanied by a male household adult
_and_ a female household adult.
    * 22 = with mom: The child was accompanied by a female household adult
but no male household adult.
    * 23 = with dad: The child was accompanied by a male household adult but
no female household adult.
    * 3 = with sibling: The child was accompanied by household children, but
no household adults or non-household members.
    * 24 = with non-household: The child was accompanied by non-household
members and no household members were on the trip.
* 'ind_3': A simplified independence variable. One of:
    * 1 = alone: Same as 1 (alone) in the full independence variable
    * 2 = with adults: Combination of these values from the full
independence variable:
        * 21 (with mom and dad)
        * 22 (with_mom)
        * 23 (with_dad)
        * 24 (with non-household)
    * 3 = with kids: same as 3 (with sibling) in the full independence variable.
* 'ind_3_alt': Same as 'ind_3a', but trips with non-household members
(indpendence = 3) are classified as trips with kids. Since we don't know if the
non-household members are kids or adults, we might want to test it both
ways and see if it effects the result.
