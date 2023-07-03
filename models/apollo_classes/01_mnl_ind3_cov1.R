library(apollo)
library(readr)
library(here)

# Initialisation ===========================
# 
# 
### Initialise code
apollo_initialise()
### Set core controls
apollo_control = list(
  modelName = "mnl_ind3_01",
  modelDescr = "MNL on kid trip data - simplified independence with first covariates",
  indivID = "id"
)

## class membership

# Data =====================================
# Read in data and do basic manipulations for coherence
# 
data <- readr::read_rds(here("data/all-purpose/usa-2017-all.rds"))
database <- data |> 
  dplyr::transmute(
    id = 1:dplyr::n(),
    # set up alternatives as named vector 
    choice = dplyr::case_when(
      mode_ind_3 == 720 ~ "drive_parent",
      mode_ind_3 == 730 ~ "drive_others",
      mode_ind_3 == 810 ~ "walk_alone",
      mode_ind_3 == 820 ~ "walk_parent",
      mode_ind_3 == 830 ~ "walk_others",
      mode_ind_3 == 910 ~ "bike_alone",
      mode_ind_3 == 920 ~ "bike_parent",
      mode_ind_3 == 930 ~ "bike_others",
      TRUE ~ as.character(NA)
    ),
    income = income_k, veh_per_driver, n_adults, non_work_mom, non_work_dad,
    age, female, distance, school, density
  ) |> 
  dplyr::filter(!is.na(choice))


# Parameters ===============================
# Create a list of all the parameters we need to estimate
#  
apollo_beta = c(
  # ASC
  asc_dp = 0, asc_do = 0, asc_wa = 0, asc_wp = 0,
  asc_wo = 0, asc_ba = 0, asc_bp = 0, asc_bo = 0,
  
  
  # Utility parameters
  # Age of the child
  beta_age_dp = 0, beta_age_do = 0, beta_age_wa = 0, beta_age_wp = 0,
  beta_age_wo = 0, beta_age_ba = 0, beta_age_bp = 0, beta_age_bo = 0,
  
  # Gender of the child
  beta_female_dp = 0, beta_female_do = 0, beta_female_wa = 0, beta_female_wp = 0,
  beta_female_wo = 0, beta_female_ba = 0, beta_female_bp = 0, beta_female_bo = 0,
  
  # Distance of the trip
  beta_distance_dp = 0, beta_distance_do = 0, beta_distance_wa = 0, beta_distance_wp = 0,
  beta_distance_wo = 0, beta_distance_ba = 0, beta_distance_bp = 0, beta_distance_bo = 0,
  
  # Density of the child's residence tract (?)
  beta_density_dp = 0, beta_density_do = 0, beta_density_wa = 0, beta_density_wp = 0,
  beta_density_wo = 0, beta_density_ba = 0, beta_density_bp = 0, beta_density_bo = 0,
  
  # School trip?
  beta_school_dp = 0, beta_school_do = 0, beta_school_wa = 0, beta_school_wp = 0,
  beta_school_wo = 0, beta_school_ba = 0, beta_school_bp = 0, beta_school_bo = 0, 
  
  # Income
  beta_income_dp = 0, beta_income_do = 0, beta_income_wa = 0, beta_income_wp = 0,
  beta_income_wo = 0, beta_income_ba = 0, beta_income_bp = 0, beta_income_bo = 0
  
)

apollo_fixed = names(apollo_beta)[grepl("wa", names(apollo_beta))]

# Model Definition =========================
# verify all the parameters and data are correct and expected
apollo_inputs = apollo_validateInputs()


# Define model probabilities and likelihood
apollo_probabilities = function(apollo_beta, apollo_inputs, functionality = "estimate") {
  
  ### Attach inputs and detach after function exit
  apollo_attach(apollo_beta, apollo_inputs)
  on.exit(apollo_detach(apollo_beta, apollo_inputs))
  ### Define settings for MNL
  mnl_settings = list(
    alternatives = c(
      walk_alone = "walk_alone", walk_others = "walk_others", walk_parent = "walk_parent",
      bike_alone = "bike_alone", bike_others = "bike_others", bike_parent = "bike_parent",
      drive_others = "drive_others", drive_parent = "drive_parent"
    ),
    choiceVar    = choice,
    explanators  = c("female", "n_adults")
  )
  
  
  ### Create list of probabilities P
  P = list()
  
  # list of alternatives with coefficient names
  J <- list(drive_parent = "dp", drive_others = "do", 
            walk_alone = "wa", walk_parent = "wp", walk_others = "wo", 
            bike_alone = "ba", bike_parent = "bp", bike_others = "bo"
  )
  V = list()
  ### compute class-specific utilities
  V = lapply(J, function(j){
    get(paste0("asc_", j)) + 
      get(paste0("beta_age_", j)) * age + 
      get(paste0("beta_female_", j)) * female + 
      get(paste0("beta_distance_", j)) * distance +
      get(paste0("beta_density_", j)) * density + 
      get(paste0("beta_school_", j)) * school + 
      get(paste0("beta_income_", j)) * income
  })
    
    
  mnl_settings$utilities <- V
    ### Compute within-class choice probabilities using MNL model
  P[["model"]] = apollo_mnl(mnl_settings, functionality)
  
  ### Prepare and return outputs of function
  P = apollo_prepareProb(P, apollo_inputs, functionality)
  return(P)
}



# Model destination ========================
setwd(here("models/apollo_classes"))
# ################################################################# #
#### MODEL ESTIMATION                                            ####
# ################################################################# #
### Estimate model
model = apollo_estimate(apollo_beta, apollo_fixed, 
                        apollo_probabilities, apollo_inputs)

### Show output in screen
apollo_modelOutput(model)

### Save output to file(s)
apollo_saveOutput(model)

