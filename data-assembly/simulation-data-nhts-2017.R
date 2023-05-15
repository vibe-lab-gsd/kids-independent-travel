## Simulation data for visualizing model results

library(tidyverse)
library(here)

# Return the most frequent category
freq_cat <- function(x) {
  uniqx <- unique(na.omit(x))
  uniqx[which.max(tabulate(match(x, uniqx)))]
}

real_data <- here("data",
                  "usa-2017.dat") |>
  read_tsv(show_col_types = FALSE)

real_data_r_vis <- real_data |>
  mutate(vary = "all") |>
  select(vary,
         income_k,
         veh_per_driver,
         n_adults,
         non_work_mom,
         non_work_dad,
         age,
         female,
         has_lil_sib,
         has_big_sib,
         distance,
         density)
         

cases_biogeme <- real_data[0,]
cases_r_vis <- real_data_r_vis[0,]

predictors <- c("log_income_k",
                "veh_per_driver",
                "n_adults",
                "non_work_mom",
                "non_work_dad",
                "age",
                "female",
                "has_lil_sib",
                "has_big_sib",
                "log_distance",
                "log_density")

unlogged <- c("income_k",
              "distance",
              "density")

n_points <- 100

for(i in 1:length(predictors)) {
  to_vary <- predictors[i]
  
  to_hold_names <- predictors[predictors != to_vary]
  
  if(substr(to_vary, 1, 4) == "log_") {
    to_vary <- substr(to_vary, 5, str_length(to_vary))
  }
  
  to_vary_vals <- real_data[[to_vary]]
  
  if(length(unique(to_vary_vals)) == 2) {
    this_cases <- tibble(id = c(1, 2))
    this_cases[, to_vary] <- unique(to_vary_vals)
  } else {
    this_cases <- tibble(id = seq(1, n_points, by = 1))
    this_cases[, to_vary] <- seq(min(to_vary_vals) +
                              ((max(to_vary_vals) - min(to_vary_vals)) / n_points),
                            max(to_vary_vals),
                            (max(to_vary_vals) - min(to_vary_vals)) / n_points)
    if (to_vary %in% unlogged) {
      this_cases[, paste0("log_", to_vary)] <- log(this_cases[[to_vary]])
    }
  }
  
  for(j in 1:length(to_hold_names)) {
    if(substr(to_hold_names[j], 1, 4) == "log_") {
      this_var <- substr(to_hold_names[j], 5, str_length(to_hold_names[j]))
      mean_this_var <- mean(real_data[[this_var]])
      this_cases[, this_var] <- rep((mean_this_var),
                               nrow(this_cases))
      this_cases[, to_hold_names[j]] <- log(this_cases[[this_var]])
    } else {
      if(length(unique(real_data[[to_hold_names[j]]])) == 2) {
        this_cases[, to_hold_names[j]] <- rep(freq_cat(real_data[[to_hold_names[j]]]),
                                         nrow(this_cases))
      } else {
        this_cases[, to_hold_names[j]] <- rep(mean(real_data[[to_hold_names[j]]]),
                                         nrow(this_cases))
      }
    }
  }
  
  this_cases <- this_cases |>
    mutate(mode = sample(unique(real_data$mode), 
                         size = nrow(this_cases), 
                         replace = TRUE),
           independence = sample(unique(real_data$independence), 
                                 size = nrow(this_cases), 
                                 replace = TRUE)) |>
    mutate(ind_3 = ifelse(independence > 20 & independence < 30, 
                          20, 
                          independence)) |>
    mutate(ind_3_alt = case_when(independence > 10 & independence < 24 ~ 20,
                                 independence == 24 ~ 30,
                                 TRUE ~ independence)) |>
    mutate(mode_ind = mode * 100 + independence,
           mode_ind_3 = mode * 100 + ind_3,
           mode_ind_3_alt = mode * 100 + ind_3_alt) |>
    mutate(av_car = 1,
           av_walk = 1,
           av_bike = 1,
           alone_avail = 1,
           with_mom_dad_avail = 1,
           with_mom_avail = 1,
           with_dad_avail = 1,
           with_non_hh_avail = 1,
           with_sib_avail = 1,
           with_adult_avail = 1,
           vary = to_vary)
           
  this_cases_biogeme <- this_cases[colnames(real_data)]
  this_cases_r_vis <- this_cases[colnames(real_data_r_vis)]
  
  cases_biogeme <- rbind(cases_biogeme, this_cases_biogeme)
  cases_r_vis <- rbind(cases_r_vis, this_cases_r_vis)
}

write_tsv(cases_biogeme,
          here("data",
               "usa-2017-test.dat"))

write_csv(cases_r_vis,
          here("data",
               "sim-data.csv"))



