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
  modelName = "NLind3",
  modelDescr = "NL on kid trip data - simplified independence",
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
  asc_dp = 0,
  asc_do = 0,
  asc_wa = 0,
  asc_wp = 0,
  asc_wo = 0,
  asc_ba = 0,
  asc_bp = 0,
  asc_bo = 0,
  
  # Utility parameters
  beta_nadults_dp = 0,
  beta_nadults_do = 0,
  beta_nadults_wa = 0,
  beta_nadults_wp = 0,
  beta_nadults_wo = 0,
  beta_nadults_ba = 0,
  beta_nadults_bp = 0,
  beta_nadults_bo = 0,
  
  # Nest parameters
  lambda_alone  = 1,
  lambda_others = 1,
  lambda_parent = 1
)

apollo_fixed = c("asc_wa",  "beta_nadults_wa")

# Model Definition =========================
# verify all the parameters and data are correct and expected
apollo_inputs = apollo_validateInputs()


# Define model probabilities and likelihood
apollo_probabilities = function(apollo_beta, apollo_inputs, functionality = "estimate") {
  
  ### Attach inputs and detach after function exit
  apollo_attach(apollo_beta, apollo_inputs)
  on.exit(apollo_detach(apollo_beta, apollo_inputs))
  
  ### Create list of probabilities P
  P = list()
  
  V = list()
  V[["drive_parent"]]  = asc_dp + beta_nadults_do * n_adults
  V[["drive_others"]]  = asc_do + beta_nadults_dp * n_adults
  V[["walk_alone"]]    = asc_wa + beta_nadults_wa * n_adults
  V[["walk_parent"]]   = asc_wp + beta_nadults_wp * n_adults
  V[["walk_others"]]   = asc_wo + beta_nadults_wo * n_adults
  V[["bike_alone"]]    = asc_ba + beta_nadults_ba * n_adults
  V[["bike_parent"]]   = asc_bp + beta_nadults_bp * n_adults
  V[["bike_others"]]   = asc_bo + beta_nadults_bo * n_adults
    
    
  ### Specify nests for NL model
  nlNests = list(root = 1, 
                 Alone  = lambda_alone, 
                 Parent = lambda_parent, 
                 Others = lambda_others)
  ### Specify tree structure for NL model
  nlStructure= list()
  nlStructure[["root"]]   = c("Alone", "Parent", "Others")
  nlStructure[["Alone"]]   = c("walk_alone","bike_alone")
  nlStructure[["Parent"]]  = c("walk_parent","bike_parent", "drive_parent")
  nlStructure[["Others"]]  = c("walk_others","bike_others", "drive_others")
    
    ### Define settings for NL model
  nl_settings = list(
    alternatives = c(
      walk_alone = "walk_alone", walk_others = "walk_others", walk_parent = "walk_parent",
      bike_alone = "bike_alone", bike_others = "bike_others", bike_parent = "bike_parent",
      drive_others = "drive_others", drive_parent = "drive_parent"
    ),
    choiceVar    = choice,
    explanators  = c("female", "n_adults"),
    utilities = V,
    nlStructure = nlStructure,
    nlNests = nlNests
  )
    
    ### Compute within-class choice probabilities using MNL model
  P[["model"]] = apollo_nl(nl_settings, functionality)
  
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

