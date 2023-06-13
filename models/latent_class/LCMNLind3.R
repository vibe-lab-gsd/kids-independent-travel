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
  modelName = "LCNLind3",
  modelDescr = "Latent class NL on kid trip data - simplified independence",
  indivID = "id"
)

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
    income_k, veh_per_driver, n_adults, non_work_mom, non_work_dad,
    age, female, school, distance, had_school,
  ) |> 
  dplyr::filter(!is.na(choice))

# Parameters ===============================
# Create a list of all the parameters we need to estimate
#  
apollo_beta = c(
  # ASC
  asc_dp_a = 0,
  asc_do_a = 0,
  asc_wa_a = 0,
  asc_wp_a = 0,
  asc_wo_a = 0,
  asc_ba_a = 0,
  asc_bp_a = 0,
  asc_bo_a = 0,
  asc_dp_b = 0,
  asc_do_b = 0,
  asc_wa_b = 0,
  asc_wp_b = 0,
  asc_wo_b = 0,
  asc_ba_b = 0,
  asc_bp_b = 0,
  asc_bo_b = 0,
  
  # Class model Parameters
  delta_a = 0,
  delta_b = 0,
  gamma_female_a = 0,
  gamma_female_b = 0,
  
  # Utility parameters
  beta_nadults_dp_a = 0,
  beta_nadults_do_a = 0,
  beta_nadults_wa_a = 0,
  beta_nadults_wp_a = 0,
  beta_nadults_wo_a = 0,
  beta_nadults_ba_a = 0,
  beta_nadults_bp_a = 0,
  beta_nadults_bo_a = 0,
  
  beta_nadults_dp_b = 0,
  beta_nadults_do_b = 0,
  beta_nadults_wa_b = 0,
  beta_nadults_wp_b = 0,
  beta_nadults_wo_b = 0,
  beta_nadults_ba_b = 0,
  beta_nadults_bp_b = 0,
  beta_nadults_bo_b = 0
  )

apollo_fixed = c("asc_wa_a", "asc_wa_b", "delta_a", "gamma_female_a", "beta_nadults_wa_a", "beta_nadults_wa_b")

# Model Definition =========================
# Define latent class components
# 
apollo_lcPars = function(apollo_beta, apollo_inputs) {
  # parameters that vary by class
  lcpars = list()
  lcpars[["asc_dp"]] = list(asc_dp_a, asc_dp_b)
  lcpars[["asc_do"]] = list(asc_do_a, asc_do_b)
  lcpars[["asc_wa"]] = list(asc_wa_a, asc_wa_b)
  lcpars[["asc_wp"]] = list(asc_wp_a, asc_wp_b)
  lcpars[["asc_wo"]] = list(asc_wo_a, asc_wo_b)
  lcpars[["asc_ba"]] = list(asc_ba_a, asc_ba_b)
  lcpars[["asc_bp"]] = list(asc_bp_a, asc_bp_b)
  lcpars[["asc_bo"]] = list(asc_bo_a, asc_bo_b)
  lcpars[["beta_nadults_dp"]] = list(beta_nadults_dp_a, beta_nadults_dp_b)
  lcpars[["beta_nadults_do"]] = list(beta_nadults_do_a, beta_nadults_do_b)
  lcpars[["beta_nadults_wa"]] = list(beta_nadults_wa_a, beta_nadults_wa_b)
  lcpars[["beta_nadults_wp"]] = list(beta_nadults_wp_a, beta_nadults_wp_b)
  lcpars[["beta_nadults_wo"]] = list(beta_nadults_wo_a, beta_nadults_wo_b)
  lcpars[["beta_nadults_ba"]] = list(beta_nadults_ba_a, beta_nadults_ba_b)
  lcpars[["beta_nadults_bp"]] = list(beta_nadults_bp_a, beta_nadults_bp_b)
  lcpars[["beta_nadults_bo"]] = list(beta_nadults_bo_a, beta_nadults_bo_b)
  
  
  ## utilities of class allocation model
  V = list()
  V[["class_a"]] = delta_a + gamma_female_a * female
  V[["class_b"]] = delta_b + gamma_female_b * female
  
  # settings for allocation model
  classAlloc_settings = list(
    classes = c(class_a = 1, class_b = 2),
    utilities = V
  )
  
  lcpars[["pi_values"]] = apollo_classAlloc((classAlloc_settings))
  
  return(lcpars)
}

# verify all the parameters and data are correct and expected
apollo_inputs = apollo_validateInputs()


# Define model probabilities and likelihood
apollo_probabilities = function(apollo_beta, apollo_inputs, functionality = "estimate") {
  
  ### Attach inputs and detach after function exit
  apollo_attach(apollo_beta, apollo_inputs)
  on.exit(apollo_detach(apollo_beta, apollo_inputs))
  
  ### Create list of probabilities P
  P = list()
  
  ### Define settings for MNL
  mnl_settings = list(
    alternatives = c(
      walk_alone = "walk_alone", walk_others = "walk_others", walk_parents = "walk_parent",
      bike_alone = "bike_alone", bike_others = "bike_others", bike_parents = "bike_parent",
      drive_others = "drive_others", drive_parents = "drive_parent"
    ),
    choiceVar    = choice,
    explanators  = c("female", "n_adults")
  )
  
  ## loop over classes
  for(s in 1:2){
    
    ### compute class-specific utilities
    V = list()
    V[["drive_parents"]] = asc_dp[[s]] + beta_nadults_do[[s]] * n_adults
    V[["drive_others"]]  = asc_do[[s]] + beta_nadults_dp[[s]] * n_adults
    V[["walk_alone"]]    = asc_wa[[s]] + beta_nadults_wa[[s]] * n_adults
    V[["walk_parents"]]  = asc_wp[[s]] + beta_nadults_wp[[s]] * n_adults
    V[["walk_others"]]   = asc_wo[[s]] + beta_nadults_wo[[s]] * n_adults
    V[["bike_alone"]]    = asc_ba[[s]] + beta_nadults_ba[[s]] * n_adults
    V[["bike_parents"]]  = asc_bp[[s]] + beta_nadults_bp[[s]] * n_adults
    V[["bike_others"]]   = asc_bo[[s]] + beta_nadults_bo[[s]] * n_adults
    
    
    mnl_settings$utilities     = V
    mnl_settings$componentName = paste0("Class_",s)
    
    ### Compute within-class choice probabilities using MNL model
    P[[paste0("Class_",s)]] = apollo_mnl(mnl_settings, functionality)
  }
  
  # compute latent class model probabilities
  lc_settings = list(inClassProb = P, classProb = pi_values)
  P[["model"]] = apollo_lc(lc_settings, apollo_inputs, functionality)
  
  ### Prepare and return outputs of function
  P = apollo_prepareProb(P, apollo_inputs, functionality)
  return(P)
}



# Model destination ========================
setwd(here("models/latent_class"))
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

