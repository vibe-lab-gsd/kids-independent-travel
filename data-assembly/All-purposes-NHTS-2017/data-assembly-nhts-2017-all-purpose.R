###############################################################################
# Data assembly - 2017 NHTS
# 
# See https://github.com/urban-stack/kids-independent-travel
# for full context
###############################################################################

library(here)
library(tidyverse)
library(downloader)
library(knitr)
library(naniar)

###################################################
# Uncomment and run below to download 2017 NHTS data. Everything except the 
# citation info is in the gitignore file, so you won't have it immediately
# upon cloning the repo.
#
# url <- "https://nhts.ornl.gov/assets/2016/download/csv.zip"
# 
# nhts_zipped <- here("nhts",
#                     "data2017",
#                     "nhts2017.zip")
# 
# nhts_dir <- here("nhts",
#                  "data2017")
# 
# download(url, nhts_zipped, mode="wb")
# unzip(nhts_zipped, exdir = nhts_dir)
##############################################################


#### Start file of data assembly notes explaining the sample and variables.
readme_path <- here("data", 
                    "all-purpose", 
                    "usa-2017-readme-all-purpose.md")

c("# Data Assembly notes",
  "",
  "## Sample",
  "",
  "Data are drawn from the 2017 National Household Travel Survey",
  "(https://nhts.ornl.gov/).",
  "",
  "### Criteria for inclusion in sample",
  "",
  "* Trip distance is shorter than 2km/1.25 miles",
  "* Traveler is between 8 and 13",
  "* School trips are excluded for children who used a school bus on the",
  "travel day",
  "* Survey does not indicate that the child drove unaccompanied (assume ",
  "these are survey coding errors)",
  "* Survey does not indicate the child traveled by car with",
  "only siblings unless the child has a sibling who is a driver.",
  "* Data not missing for any outcome or predictor variables",
  "* Trips with the purpose of transfering to another mode are included",
  "as separate trips.",
  "",

  "## Variables",
  "",
  "### Identifiers",
  "* HOUSEID: A unique identifier for the household",
  "* person_hh: A unique identifier for the person",
  "",
  "### Outcome variables",
  "* 'mode': One of", 
  "    * 7 = car",
  "    * 8 = walk", 
  "    * 9 = bike",
  "* 'independence': (string) For purposes of this analysis, we describe all",
  "female household adults as moms, all male household adults as dads, and all",
  "household children as siblings. Also note that NHTS codes all household",
  "members as either male or female. We know how many non-household members",
  "are on a trip, but we don't know their ages, genders, or drivers status.",
  "The full independence variable takes one",
  "of the following 6 values to describe who was with the child on their trip", 
  "to school:",
  "    * 10 = alone: There was only one person (the child) on the trip.",
  "    * 21 = with mom and dad: The child was accompanied by a male household adult",
  "_and_ a female household adult.",
  "    * 22 = with mom: The child was accompanied by a female household adult",
  "but no male household adult.",
  "    * 23 = with dad: The child was accompanied by a male household adult but",
  "no female household adult.",
  "no household adults or non-household members.",
  "    * 24 = with non-household: The child was accompanied by non-household",
  "members and no household members were on the trip.",
  "    * 30 = with sibling: The child was accompanied by household children, but",
  "* 'ind_3': A simplified independence variable. One of:",
  "    * 10 = alone: Same as 1 (alone) in the full independence variable",
  "    * 20 = with adults: Combination of these values from the full",
  "independence variable:",
  "        * 21 (with mom and dad)", 
  "        * 22 (with mom)",
  "        * 23 (with dad)", 
  "        * 24 (with non-household)",
  "    * 30 = with kids: same as 3 (with sibling) in the full independence variable.",
  "* 'ind_3_alt': Same as 'ind_3a', but trips with non-household members", 
  "(indpendence = 3) are classified as trips with kids. Since we don't know if the",
  "non-household members are kids or adults, we might want to test it both",
  "ways and see if it effects the result.",
  "* 'mode_ind': Combination of mode and the full independence variable. Takes",
  "the following values:",
  "    * 721 = car with mom and dad",
  "    * 722 = car with mom",
  "    * 723 = car with dad",
  "    * 724 = car with non-household",
  "    * 730 = car with sibling",
  "    * 810 = walk alone",
  "    * 821 = walk with mom and dad",
  "    * 822 = walk with mom",
  "    * 823 = walk with dad",
  "    * 824 = walk with non-household",
  "    * 830 = walk with sibling",
  "    * 910 = bike alone",
  "    * 921 = bike with mom and dad",
  "    * 922 = bike with mom",
  "    * 923 = bike with dad",
  "    * 924 = bike with non-household",
  "    * 930 = bike with sibling",
  "* 'mode_ind_3': Combination of mode and the simplified independence",
  "variable. Takes the following values",
  "    *720 = car with adult",
  "    *730 = car with kid",
  "    *810 = walk alone",
  "    *820 = walk with adults",
  "    *830 = walk with kids",
  "    *910 = bike alone",
  "    *920 = bike with adults",
  "    *930 = bike with kids",
  "* 'mode_ind_3_alt': Combination of mode and the simplified independence",
  "variable that classifies non-household members as kids. Same categories",
  "as 'mode_ind_3.",
  "",
  "### Availability variables",
  "",
  "'av_car', 'av_walk', and 'av_bike' indicate the trips for which travel by",
  "car, walking, or bike is available. We are assuming that these three modes",
  "are available for all children in the sample (even if there is not car in",
  "the household, since some children in the sample in zero-vehicle households",
  "_do_ travel by car) so this value is set to one for all cases.",
  "",
  "The following variables indicate the availability of independence", 
  "alternatives:",
  "",
  "* alone_avail: TRUE/1 for all trips",
  "* with_mom_dad_avail: True if there is both a female and a male adult in",
  "the household.",
  "* with_mom_avail: True if there is a female adult in the household",
  "* with_dad_avail: True if there is a male adult in the household",
  "* with_non_hh_avail: True for all trips",
  "* with_sib_avail: True if there are any other children in the household",
  "* with_adult_avail: True for all trips",
  "",
  "### Predictor variables",
  "",
  "* Household-level variables",
  "    * income_k: NHTS codes income in one of 11 income categories. We",
  "convert this to a continuous variable by assigning households in each",
  "category the mid-point value of that category. The highest income category",
  "is for incomes greater than $200,000 per year. We assign an income of", 
  "$250,000 to that category. log_income_k is the natural log of income_k.",
  "    * veh_per_driver: We divide the number of household vehicles by the",
  "number of household drivers. We assign a value of zero to households with",
  "zero drivers",
  "    * n_adults: The number of household adults",
  "    * non_work_mom: A binary variable indicating whether there is a female", 
  "adult in the household who is not a worker",
  "    * non_work_dad: A binary variable indicating whether there is a male", 
  "adult in the household who is not a worker",
  "* Individual-level variables",
  "    * age: The child's age",
  "    * female: A binary variable indicating whether the child is female",
  "    * has_lil_sib: A binary variable indicating whether there are any",
  "younger children in the household (includes children who are the same",
  "age as the respondent).",
  "    * has_big_sib: A binary variable indicating whether there are any",
  "older children in the household",
  "* Trip-level variables",
  "    * school: A binary variable indicating whether this is a school trip",
  "    * distance: Trip distance in kilometers. The NHTS records distance",
  "in miles and these are converted to kilometers by multiplying by 1.609.",
  "log_distance is the natural log of distance.",
  "    * density: The approximate population density of the census block", 
  "in which the trip begins or ends (whichever is higher). NHTS reports", 
  "this value in people per square mile. We convert to people per square",
  "kilometer by dividing by 2.59. log_density is the natural log of density.",
  "* Travel-day variables",
  "    * had_school: Child attended school",
  "    * Distance from home to school (km)",
  "    * n_non_school_trips: Number of non-school trips that day",
  "    * avg_trip_dist: Average length of trips that day (km)",
  "") |>
  write_lines(readme_path, append = FALSE)

#### Load NHTS trip and person files

trips <- here("nhts",
              "data2017", 
              "trippub.csv") |>
  read_csv(show_col_types = FALSE) 

people <- here("nhts",
               "data2017", 
               "perpub.csv") |>
  read_csv(show_col_types = FALSE) |>
  mutate(person_hh = paste(PERSONID, HOUSEID, sep = "-"))


#### Assemble data
hh_ages <- people |>
  select(HOUSEID, PERSONID, R_AGE) |>
  pivot_wider(names_from = PERSONID,
              names_prefix = "age_",
              values_from = R_AGE)

hh_genders <- people %>%
  select(HOUSEID, PERSONID, R_SEX_IMP) |>
  pivot_wider(names_from = PERSONID,
              names_prefix = "gender_",
              values_from = R_SEX_IMP)

relationships <- people |>
  mutate(adult = R_AGE > 17,
         mom = R_AGE > 17 & R_SEX_IMP == "02",
         dad = R_AGE > 17 & R_SEX_IMP != "02",
         kid_age = ifelse(R_AGE < 18, R_AGE, -2),
         R_AGE = ifelse(R_AGE < 0, 999, R_AGE),
         non_worker_mom = R_AGE > 17 & WORKER != "01" & R_SEX_IMP == "02",
         non_worker_dad = R_AGE > 17 & WORKER != "01" & R_SEX_IMP != "02",
         driver_mom = R_AGE > 17 & DRIVER == "01" & R_SEX_IMP == "02",
         driver_dad = R_AGE > 17 & DRIVER == "01" & R_SEX_IMP != "02",
         driver_sib = R_AGE < 18 & DRIVER == "01") |>
  group_by(HOUSEID) |>
  mutate(n_adults = sum(adult),
         has_mom = sum(mom) > 0,
         has_dad = sum(dad) > 0,
         driver_mom = sum(driver_mom) > 0,
         driver_dad = sum(driver_dad) > 0,
         driver_sib = sum(driver_sib) > 0,
         num_records = n(),
         non_work_mom = sum(non_worker_mom) > 0,
         non_work_dad = sum(non_worker_dad) > 0) |>
  mutate(youngest_kid = ifelse(num_records > HHSIZE, 1, min(R_AGE)),
         oldest_kid = max(kid_age),
         n_children = HHSIZE - n_adults) |>
  mutate(has_big_sib = n_children > 1 & R_AGE != oldest_kid) |>
  mutate(has_lil_sib = n_children > 1 & (R_AGE != youngest_kid | !has_big_sib)) |>
  mutate(person_hh = paste(PERSONID, HOUSEID, sep = "-")) |>
  mutate(school_dist = 1.609 * DISTTOSC17) |>
  ungroup() |>
  select(HOUSEID,
         person_hh, 
         has_lil_sib, 
         has_big_sib,
         n_adults,
         has_mom, 
         has_dad,
         non_work_mom,
         non_work_dad,
         driver_mom,
         driver_dad,
         driver_sib,
         school_dist) 

kid_short_trips <- trips |>
  mutate(include_trip = (R_AGE > 7 & 
                           R_AGE < 14 &
                           TRPMILES > 0 &
                           TRPMILES < 1.25)) |>
  mutate(WHYTO = case_when(WHYTO == "07" ~ "transfer", 
                           WHYTO == "08" ~ "school",
                           TRUE ~ WHYTO),
         WHYFROM = case_when(WHYFROM == "07" ~ "transfer", 
                             WHYFROM == "08" ~ "school",
                             TRUE ~ WHYFROM),
         mode = case_when(TRPTRANS == "10" ~ 1, # school bus
                          TRPTRANS == "03" ~ 7, # car
                          TRPTRANS == "04" ~ 7,
                          TRPTRANS == "05" ~ 7,
                          TRPTRANS == "06" ~ 7,
                          TRPTRANS == "18" ~ 7,
                          TRPTRANS == "01" ~ 8, # walk
                          TRPTRANS == "02" ~ 9, # bike
                          TRUE ~ 5)) |>
  mutate(trip_person_hh = paste(TDTRPNUM, PERSONID, HOUSEID, sep = "-")) |>
  mutate(person_hh = paste(PERSONID, HOUSEID, sep = "-")) |>
  mutate(school = WHYTO == "school" | WHYFROM == "school") |>
  group_by(person_hh) |>
  mutate(can_sch_bus = sum(mode == 1) > 0 & school,
         n_non_school_trips = sum(!school),
         had_school = sum(school) > 1,
         avg_trip_dist = 1.609 * mean(TRPMILES)) |>
  ungroup() |>
  filter(!school | !can_sch_bus) |>
  filter(include_trip > 0) |>
  left_join(hh_ages) |>
  left_join(hh_genders) |>
  mutate(alone = NUMONTRP == 1,
         with_mom = 
           (ONTD_P1 == "01" & age_01 > 17 & gender_01 == "02") |
           (ONTD_P2 == "01" & age_02 > 17 & gender_02 == "02") |
           (ONTD_P3 == "01" & age_03 > 17 & gender_03 == "02") |
           (ONTD_P4 == "01" & age_04 > 17 & gender_04 == "02") |
           (ONTD_P5 == "01" & age_05 > 17 & gender_05 == "02") |
           (ONTD_P6 == "01" & age_06 > 17 & gender_06 == "02") |
           (ONTD_P7 == "01" & age_07 > 17 & gender_07 == "02") |
           (ONTD_P8 == "01" & age_08 > 17 & gender_08 == "02") |
           (ONTD_P9 == "01" & age_09 > 17 & gender_09 == "02") |
           (ONTD_P10 == 1 & age_10 > 17 & gender_10 == "02") |
           (ONTD_P11 == 1 & age_11 > 17 & gender_11 == "02") |
           (ONTD_P12 == 1 & age_12 > 17 & gender_12 == "02") |
           (ONTD_P13 == 1 & age_13 > 17 & gender_13 == "02"),
         with_dad = 
           (ONTD_P1 == "01" & age_01 > 17 & gender_01 != "02") |
           (ONTD_P2 == "01" & age_02 > 17 & gender_02 != "02") |
           (ONTD_P3 == "01" & age_03 > 17 & gender_03 != "02") |
           (ONTD_P4 == "01" & age_04 > 17 & gender_04 != "02") |
           (ONTD_P5 == "01" & age_05 > 17 & gender_05 != "02") |
           (ONTD_P6 == "01" & age_06 > 17 & gender_06 != "02") |
           (ONTD_P7 == "01" & age_07 > 17 & gender_07 != "02") |
           (ONTD_P8 == "01" & age_08 > 17 & gender_08 != "02") |
           (ONTD_P9 == "01" & age_09 > 17 & gender_09 != "02") |
           (ONTD_P10 == 1 & age_10 > 17 & gender_10 != "02") |
           (ONTD_P11 == 1 & age_11 > 17 & gender_11 != "02") |
           (ONTD_P12 == 1 & age_12 > 17 & gender_12 != "02") |
           (ONTD_P13 == 1 & age_13 > 17 & gender_13 != "02"),
         hh_only = NUMONTRP == NONHHCNT+1) |>
  left_join(relationships) |>
  mutate(independence = case_when(with_mom & with_dad ~ 21,
                                  with_mom ~ 22,
                                  with_dad ~ 23,
                                  alone ~ 10,
                                  NONHHCNT == 0 ~ 30,
                                  TRUE ~ 24)) |>
  mutate(ind_3 = ifelse(independence > 20 & independence < 30, 
                        20, independence)) |>
  mutate(ind_3_alt = case_when(independence > 10 & independence < 24 ~ 20,
                               independence == 24 ~ 30,
                               TRUE ~ independence)) |>
  filter(!(mode == 7 & independence == 10),
         !(mode == 7 & independence == 30 & !driver_sib)) |>
  mutate(mode_ind = mode * 100 + independence,
         mode_ind_3 = mode * 100 + ind_3,
         mode_ind_3_alt = mode * 100 + ind_3_alt) |>
  mutate(veh_per_driver = ifelse(DRVRCNT > 0, HHVEHCNT/DRVRCNT, 0)) |>
  mutate(income_k = case_when(HHFAMINC == "01" ~ 5,
                              HHFAMINC == "02" ~ 12.5,
                              HHFAMINC == "03" ~ 20,
                              HHFAMINC == "04" ~ 30,
                              HHFAMINC == "05" ~ 42.5,
                              HHFAMINC == "06" ~ 62.5,
                              HHFAMINC == "07" ~ 87.5,
                              HHFAMINC == "08" ~ 112.5,
                              HHFAMINC == "09" ~ 137.5,
                              HHFAMINC == "10" ~ 175,
                              HHFAMINC == "11" ~ 250,
                              TRUE ~ -9)) |>
  filter(income_k > 0) |>
  mutate(max_od_dens = ifelse(DBPPOPDN > OBPPOPDN, DBPPOPDN, OBPPOPDN)) |>
  filter(max_od_dens > 0) |>
  rename(age = R_AGE) |>
  mutate(female = as.numeric(R_SEX_IMP == "02"),
         has_mom = as.numeric(has_mom),
         has_dad = as.numeric(has_dad),
         non_work_mom = as.numeric(non_work_mom),
         non_work_dad = as.numeric(non_work_dad),
         has_lil_sib = as.numeric(has_lil_sib),
         has_big_sib = as.numeric(has_big_sib),
         distance = TRPMILES * 1.609,
         density = max_od_dens / 2.59) |>
  mutate(with_mom_avail = ifelse(has_mom == 1, 1, 0),
         with_dad_avail = ifelse(has_dad ==1, 1, 0),
         with_mom_dad_avail = ifelse(has_mom + has_dad == 2, 1, 0),
         with_sib_avail = ifelse(has_lil_sib + has_big_sib > 0, 1, 0)) |>
  mutate(log_income_k = log(income_k),
         log_distance = log(distance),
         log_density = log(density),
         av_car = 1,
         av_walk = 1,
         av_bike = 1,
         alone_avail = 1,
         with_non_hh_avail = 1,
         with_adult_avail = 1) |>
  select(HOUSEID,
         person_hh,
         mode,
         TRPTRANS,
         independence,
         ind_3,
         ind_3_alt,
         mode_ind,
         mode_ind_3,
         mode_ind_3_alt,
         income_k,
         log_income_k,
         veh_per_driver,
         n_adults,
         non_work_mom,
         non_work_dad,
         age,
         female,
         has_lil_sib,
         has_big_sib,
         school,
         distance,
         log_distance,
         density,
         log_density,
         school_dist,
         avg_trip_dist,
         n_non_school_trips,
         had_school,
         av_car,
         av_walk,
         av_bike,
         alone_avail,
         with_mom_dad_avail,
         with_mom_avail,
         with_dad_avail,
         with_non_hh_avail,
         with_sib_avail,
         with_adult_avail)

kid_short_trips |>
  filter(mode == 5) |>
  mutate(Mode = case_when(TRPTRANS == "07" ~ "Golf cart or segway",
                          TRPTRANS == "08" ~ "Moped or motorcycle",
                          TRPTRANS == "09" ~ "RV, motorhome, ATV, or snowmobile",
                          TRPTRANS == "97" ~ "Unspecified",
                          TRPTRANS == "11" ~ "Transit", 
                          TRPTRANS == "12" ~ "Transit",
                          TRPTRANS == "13" ~ "Transit",
                          TRPTRANS == "14" ~ "Transit",
                          TRPTRANS == "15" ~ "Transit",
                          TRPTRANS == "16" ~ "Transit",
                          TRPTRANS == "17" ~ "Transit",
                          TRPTRANS == "20" ~ "Transit",
                          TRUE ~ "no idea")) |>
  group_by(Mode) |>
  summarise(`Number of trips` = n()) |>
  select(Mode, `Number of trips`) |>
  kable(format = 'pipe',
        caption = "Modes excluded from analysis") |>
  write_lines(readme_path, append = TRUE) 

kid_short_trips <- kid_short_trips |>
  filter(mode != 5) |>
  select(-TRPTRANS)

c("## Summary statistics", 
  "") |>
  write_lines(readme_path, append = TRUE) 

tibble(Unit = c("Households",
                "Children",
                "Trips"),
       Sample = c(length(unique(kid_short_trips$HOUSEID)),
                  length(unique(kid_short_trips$person_hh)),
                  nrow(kid_short_trips))) |>
  kable(format = 'pipe',
        caption = "Sample size") |>
  write_lines(readme_path, append = TRUE) 

c("",
  "### Outcomes") |>
  write_lines(readme_path, append = TRUE) 

write_lines("", readme_path, append = TRUE) 

mode_ind_table_count <- kid_short_trips |>
  group_by(independence, mode) |>
  summarise(n = n()) |>
  ungroup() |>
  pivot_wider(names_from = mode, values_from = n) |>
  replace_na(list(`7` = 0)) |>
  cbind(`-` = c("Alone", 
                  "With mom and dad", 
                  "With mom",
                  "With dad",
                  "With non-household",
                  "With siblings")) |>
  rename(Car = `7`,
         Walk = `8`,
         Bike = `9`,) |>
  select(`-`,
         Car,
         Bike, 
         Walk) |>
  mutate(Total = Car + Bike + Walk) |>
  rbind(tibble(`-` = "Total",
               Car = sum(kid_short_trips$mode == 7),
               Walk = sum(kid_short_trips$mode == 8),
               Bike = sum(kid_short_trips$mode ==9),
               Total = nrow(kid_short_trips))) 
  
mode_ind_table_pct <- mode_ind_table_count |>
  mutate(across(-`-`, ~ paste0(round(.x * 100/ nrow(kid_short_trips),1), "%")))

kable(mode_ind_table_count,
      format = 'pipe',
      caption = "Number of trips in sample by mode and (full) independence") |>
  write_lines(readme_path, append = TRUE) 

write_lines("", readme_path, append = TRUE) 

kable(mode_ind_table_pct,
      caption = "Share of trips in sample by mode and (full) independence") |>
  write_lines(readme_path, append = TRUE) 

write_lines("", readme_path, append = TRUE) 

mode_ind3_table_count <- kid_short_trips |>
  group_by(ind_3, mode) |>
  summarise(n = n()) |>
  ungroup() |>
  pivot_wider(names_from = mode, values_from = n) |>
  replace_na(list(`7` = 0)) |>
  cbind(`-` = c("Alone", 
                "With adults",
                "With kids")) |>
  rename(Car = `7`,
         Walk = `8`,
         Bike = `9`) |>
  select(`-`,
         Car,
         Bike, 
         Walk) |>
  mutate(Total = Car + Bike + Walk) |>
  rbind(tibble(`-` = "Total",
               Car = sum(kid_short_trips$mode == 7),
               Walk = sum(kid_short_trips$mode == 8),
               Bike = sum(kid_short_trips$mode ==9),
               Total = nrow(kid_short_trips))) 

mode_ind3_table_pct <- mode_ind3_table_count |>
  mutate(across(-`-`, ~ paste0(round(.x * 100/ nrow(kid_short_trips),1), "%")))

kable(mode_ind3_table_count,
      format = 'pipe',
      caption = "Number of trips in sample by mode and (simplified) independence") |>
  write_lines(readme_path, append = TRUE) 

write_lines("", readme_path, append = TRUE) 

kable(mode_ind3_table_pct,
      format = 'pipe',
      caption = "Share of trips in sample by mode and (simplified) independence") |>
  write_lines(readme_path, append = TRUE) 

write_lines("", readme_path, append = TRUE) 

mode_ind3alt_table_count <- kid_short_trips |>
  group_by(ind_3_alt, mode) |>
  summarise(n = n()) |>
  ungroup() |>
  pivot_wider(names_from = mode, values_from = n) |>
  replace_na(list(`7` = 0)) |>
  cbind(`-` = c("Alone", 
                "With adults",
                "With kids")) |>
  rename(Car = `7`,
         Walk = `8`,
         Bike = `9`) |>
  select(`-`,
         Car,
         Bike, 
         Walk) |>
  mutate(Total = Car + Bike + Walk) |>
  rbind(tibble(`-` = "Total",
               Car = sum(kid_short_trips$mode == 7),
               Walk = sum(kid_short_trips$mode == 8),
               Bike = sum(kid_short_trips$mode ==9),
               Total = nrow(kid_short_trips))) 

mode_ind3alt_table_pct <- mode_ind3alt_table_count |>
  mutate(across(-`-`, ~ paste0(round(.x * 100/ nrow(kid_short_trips),1), "%")))

kable(mode_ind3alt_table_count,
      format = 'pipe',
      caption = "Number of trips in sample by mode and (alternative simplified) independence") |>
  write_lines(readme_path, append = TRUE) 

write_lines("", readme_path, append = TRUE) 

kable(mode_ind3alt_table_pct,
      format = 'pipe',
      caption = "Share of trips in sample by mode and (alternative simplified) independence") |>
  write_lines(readme_path, append = TRUE) 

write_lines("", readme_path, append = TRUE) 

c("### Choice availability","") |>
  write_lines(readme_path, append = TRUE)

tibble(`Full independence variable` = c("Alone",
                                     "With mom and dad",
                                     "With mom",
                                     "With dad",
                                     "With non-household",
                                     "With siblings"),
    `Percent selected` = c(mean(kid_short_trips$independence == 10),
                           mean(kid_short_trips$independence == 21),
                           mean(kid_short_trips$independence == 22),
                           mean(kid_short_trips$independence == 23),
                           mean(kid_short_trips$independence == 24),
                           mean(kid_short_trips$independence == 30)),
    `Percent available` = c(1,
                            mean(kid_short_trips$with_mom_dad_avail),
                            mean(kid_short_trips$with_mom_avail),
                            mean(kid_short_trips$with_dad_avail),
                            1,
                            mean(kid_short_trips$with_sib_avail))) |>
  mutate(`Percent selected` = paste0(round(`Percent selected`*100), "%"),
         `Percent available` = paste0(round(`Percent available`*100), "%")) |>
  kable(format = 'pipe',
        caption = "Prevalence and availability of full independence choices") |>
  write_lines(readme_path, append = TRUE) 

c("","### Predictors", "") |>
  write_lines(readme_path, append = TRUE) 

kid_short_trips |>
  select(-HOUSEID,
         -person_hh,
         -mode,
         -independence,
         -ind_3,
         -ind_3_alt,
         -mode_ind,
         -mode_ind_3,
         -mode_ind_3_alt,
         -av_bike,
         -av_car,
         -av_walk,
         -alone_avail,
         -with_adult_avail,
         -with_dad_avail,
         -with_mom_avail,
         -with_mom_dad_avail,
         -with_non_hh_avail,
         -with_sib_avail,
         -log_income_k,
         -log_distance,
         -log_density) |>
  pivot_longer(cols = everything(),
               names_to = "Predictor",
               values_to = "Value") |>
  group_by(Predictor) |>
  summarise(Mean = mean(Value),
            `Standard Deviation` = ifelse(length(unique(Value)) == 2, 
                                          999,
                                          sd(Value))) |>
  replace_with_na(list(`Standard Deviation` = 999)) |>
  kable(format = 'pipe', digits = 3,
        caption = "Descriptive statistics of predictor variables") |>
  write_lines(readme_path, append = TRUE) 

kid_short_trips |>
  write_tsv(file = here("data",
                        "all-purpose",
                        "usa-2017-all.dat"))
