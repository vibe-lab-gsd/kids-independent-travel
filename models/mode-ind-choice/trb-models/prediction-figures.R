library(tidyverse)
library(here)
library(patchwork)

## Read in test data
test_data <- here("data",
                  "only-school",
                  "usa-2017-test.dat") |>
  read_tsv()

## Read mode results
mode_preds <- here("models",
                   "mode-ind-choice",
                   "trb-models",
                   "biogeme_preds_mode.csv") |>
  read_csv()

## Read ind results
ind_preds <- here("models",
                   "mode-ind-choice",
                   "trb-models",
                   "biogeme_preds_ind.csv") |>
  read_csv()

ind_data <- cbind(test_data, ind_preds)

## Read combined results

nest_preds <- here("models",
                   "mode-ind-choice",
                   "trb-models",
                   "biogeme_preds_ind-nests.csv") |>
  read_csv()

nest_data <- cbind(test_data, nest_preds)

############## mode plots

vary_inc_preds_mode <- mode_data |>
  select(income_k, `Prob. car`, `Prob. walk`, `Prob. bike`) |>
  filter(income_k != 97.602533172497) |>
  pivot_longer(cols = -income_k, names_to = "alternative", names_prefix = "Prob. ")|>
  mutate(alternative = factor(alternative, levels = c("car", "bike", "walk")))

inc_plot_mode <- ggplot(vary_inc_preds_mode) +
  geom_area(aes(x = income_k, 
                y = value,
                fill = alternative),
            alpha = 0.6) +
  scale_fill_manual(values = c("black",
                               "darkgray",
                               "lightgray"),
                    labels = c("Car",
                               "Bike",
                               "Walk"),
                    name = "Mode") +
  scale_x_continuous(name = "Income\n($1 000 USD)",
                     breaks = c(100, 200)) +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

vary_veh_preds_mode <- mode_data |>
  select(veh_per_driver, `Prob. car`, `Prob. walk`, `Prob. bike`) |>
  filter(veh_per_driver <= 1.08 | veh_per_driver >= 1.2) |>
  pivot_longer(cols = -veh_per_driver, names_to = "alternative", names_prefix = "Prob. ")|>
  mutate(alternative = factor(alternative, levels = c("car", "bike", "walk")))

veh_plot_mode <- ggplot(vary_veh_preds_mode) +
  geom_area(aes(x = veh_per_driver, 
                y = value,
                fill = alternative),
            alpha = 0.6) +
  scale_fill_manual(values = c("black",
                               "darkgray",
                               "lightgray"),
                    labels = c("Car",
                               "Bike",
                               "Walk"),
                    name = "Mode") +
  scale_x_continuous(name = "Vehicles per driver",
                     limits = c(0, 2),
                     breaks = seq(0,2,by=1)) +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

vary_age_preds_mode <- mode_data |>
  select(age, `Prob. car`, `Prob. walk`, `Prob. bike`) |>
  filter(age <= 10.15 | age >= 10.2) |>
  pivot_longer(cols = -age, names_to = "alternative", names_prefix = "Prob. ") |>
  mutate(alternative = factor(alternative, levels = c("car", "bike", "walk")))

age_plot_mode <- ggplot(vary_age_preds_mode) +
  geom_area(aes(x = age, 
                y = value,
                fill = alternative),
            alpha = 0.6) +
  scale_fill_manual(values = c("black",
                               "darkgray",
                               "lightgray"),
                    labels = c("Car",
                               "Bike",
                               "Walk"),
                    name = "Mode") +
  scale_x_continuous(name = "Age") +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

vary_female_preds_mode <- mode_data |>
  filter(income_k == 97.602533172497 & 
           (age > 10.15 & age < 10.2) &
           (veh_per_driver > 1.08 & veh_per_driver < 1.2) &
           (n_adults > 2.02 & n_adults < 2.08) &
           (distance > 1.087 & distance < 1.1) &
           (density > 2447 & density < 2563) &
           non_work_mom == 0 &
           non_work_dad == 0 &
           has_big_sib == 0 &
           has_lil_sib == 0) |>
  group_by(female) |>
  summarise(`Prob. car` = mean(`Prob. car`), 
            `Prob. walk` = mean(`Prob. walk`), 
            `Prob. bike` = mean(`Prob. bike`)) |>
  pivot_longer(cols = -female, names_to = "alternative", names_prefix = "Prob. ")|>
  mutate(alternative = factor(alternative, levels = c("car", "bike", "walk")),
         female = as.character(female))

female_plot_mode <- ggplot(vary_female_preds_mode) +
  geom_bar(aes(x = female, 
               y = value,
               fill = alternative),
           stat = "identity",
           position = position_stack(),
           alpha = 0.6) +
  scale_fill_manual(values = c("black",
                               "darkgray",
                               "lightgray"),
                    labels = c("Car",
                               "Bike",
                               "Walk"),
                    name = "Mode") +
  scale_x_discrete(name = "Gender",
                   labels = c("Boys",
                              "Girls")) +
  scale_y_continuous(name = "Probability") +
  theme_minimal() 

vary_dist_preds_mode <- mode_data |>
  select(distance, `Prob. car`, `Prob. walk`, `Prob. bike`) |>
  filter(distance <= 1.09 | distance >= 1.1) |>
  pivot_longer(cols = -distance, names_to = "alternative", names_prefix = "Prob. ") |>
  mutate(alternative = factor(alternative, levels = c("car", "bike", "walk")))

dist_plot_mode <- ggplot(vary_dist_preds_mode) +
  geom_area(aes(x = distance, 
                y = value,
                fill = alternative),
            alpha = 0.6) +
  scale_fill_manual(values = c("black",
                               "darkgray",
                               "lightgray"),
                    labels = c("Car",
                               "Bike",
                               "Walk"),
                    name = "Mode") +
  scale_x_continuous(name = "Trip distance (km)",
                     breaks = seq(0, 2, by=0.5),
                     labels = seq(0, 2, by = 0.5)) +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

vary_dens_preds_mode <- mode_data |>
  select(density, `Prob. car`, `Prob. walk`, `Prob. bike`) |>
  filter(density <= 2447 | density >= 2563) |>
  pivot_longer(cols = -density, names_to = "alternative", names_prefix = "Prob. ") |>
  mutate(alternative = factor(alternative, levels = c("car", "bike", "walk")))

dens_plot_mode <- ggplot(vary_dens_preds_mode) +
  geom_area(aes(x = density, 
                y = value,
                fill = alternative),
            alpha = 0.6) +
  scale_fill_manual(values = c("black",
                               "darkgray",
                               "lightgray"),
                    labels = c("Car",
                               "Bike",
                               "Walk"),
                    name = "Mode") +
  scale_x_continuous(name = "Population density\n(people per square km)",
                     breaks = c(5000, 10000)) +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

inc_plot_mode + veh_plot_mode + 
  age_plot_mode + female_plot_mode +
  dist_plot_mode + dens_plot_mode + 
  plot_layout(guides = 'collect')

ggsave(filename = here("models",
                       "mode-ind-choice",
                       "trb-models",
                       "prob_plots_mode.png"), 
       width = 6.25, height = 4, units = "in", dpi = 300)

########## Independence

vary_non_work_mom_preds_ind <- ind_data |>
  filter(income_k == 97.602533172497 & 
           (age > 10.15 & age < 10.2) &
           (veh_per_driver > 1.08 & veh_per_driver < 1.2) &
           (n_adults > 2.02 & n_adults < 2.08) &
           (distance > 1.087 & distance < 1.1) &
           (density > 2447 & density < 2563) &
           female == 0 &
           non_work_dad == 0 &
           has_big_sib == 0 &
           has_lil_sib == 0) |>
  group_by(non_work_mom) |>
  summarise(`Prob. adult` = mean(`Prob. adult`), 
            `Prob. non-hh` = mean(`Prob. non-hh`), 
            `Prob. alone` = mean(`Prob. alone`)) |>
  pivot_longer(cols = -non_work_mom, names_to = "alternative", names_prefix = "Prob. ")|>
  mutate(alternative = factor(alternative, levels = c("adult", "non-hh", "alone")),
         non_work_mom = as.character(non_work_mom))

non_work_mom_plot_ind <- ggplot(vary_non_work_mom_preds_ind) +
  geom_bar(aes(x = non_work_mom, 
               y = value,
               fill = alternative),
           stat = "identity",
           position = position_stack(),
           alpha = 0.6) +
  scale_fill_manual(values = c("#7570B3",
                               "#D95F02",
                               "#1B9E77"),
                    labels = c("With parent",
                               "With others",
                               "Alone"),
                    name = "Independence") +
  scale_x_discrete(name = "Non-working mother",
                   labels = c("No",
                              "Yes")) +
  scale_y_continuous(name = "Probability") +
  theme_minimal() 

vary_age_preds_ind <- ind_data |>
  select(age, `Prob. adult`, `Prob. non-hh`, `Prob. alone`) |>
  filter(age <= 10.15 | age >= 10.2) |>
  pivot_longer(cols = -age, names_to = "alternative", names_prefix = "Prob. ") |>
  mutate(alternative = factor(alternative, levels = c("adult", "non-hh", "alone")))

age_plot_ind <- ggplot(vary_age_preds_ind) +
  geom_area(aes(x = age, 
                y = value,
                fill = alternative),
            alpha = 0.6) +
  scale_fill_manual(values = c("#7570B3",
                               "#D95F02",
                               "#1B9E77"),
                    labels = c("With parent",
                               "With others",
                               "Alone"),
                    name = "Independence") +
  scale_x_continuous(name = "Age") +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

vary_female_preds_ind <- ind_data |>
  filter(income_k == 97.602533172497 & 
           (age > 10.15 & age < 10.2) &
           (veh_per_driver > 1.08 & veh_per_driver < 1.2) &
           (n_adults > 2.02 & n_adults < 2.08) &
           (distance > 1.087 & distance < 1.1) &
           (density > 2447 & density < 2563) &
           non_work_mom == 0 &
           non_work_dad == 0 &
           has_big_sib == 0 &
           has_lil_sib == 0) |>
  group_by(female) |>
  summarise(`Prob. adult` = mean(`Prob. adult`), 
            `Prob. non-hh` = mean(`Prob. non-hh`), 
            `Prob. alone` = mean(`Prob. alone`)) |>
  pivot_longer(cols = -female, names_to = "alternative", names_prefix = "Prob. ")|>
  mutate(alternative = factor(alternative, levels = c("adult", "non-hh", "alone")),
         female = as.character(female))

female_plot_ind <- ggplot(vary_female_preds_ind) +
  geom_bar(aes(x = female, 
               y = value,
               fill = alternative),
           stat = "identity",
           position = position_stack(),
           alpha = 0.6) +
  scale_fill_manual(values = c("#7570B3",
                               "#D95F02",
                               "#1B9E77"),
                    labels = c("With parent",
                               "With others",
                               "Alone"),
                    name = "Independence") +
  scale_x_discrete(name = "Gender",
                   labels = c("Boys",
                              "Girls")) +
  scale_y_continuous(name = "Probability") +
  theme_minimal() 

vary_old_sib_preds_ind <- ind_data |>
  filter(income_k == 97.602533172497 & 
           (age > 10.15 & age < 10.2) &
           (veh_per_driver > 1.08 & veh_per_driver < 1.2) &
           (n_adults > 2.02 & n_adults < 2.08) &
           (distance > 1.087 & distance < 1.1) &
           (density > 2447 & density < 2563) &
           non_work_mom == 0 &
           non_work_dad == 0 &
           female == 0 &
           has_lil_sib == 0) |>
  group_by(has_big_sib) |>
  summarise(`Prob. adult` = mean(`Prob. adult`), 
            `Prob. non-hh` = mean(`Prob. non-hh`), 
            `Prob. alone` = mean(`Prob. alone`)) |>
  pivot_longer(cols = -has_big_sib, names_to = "alternative", names_prefix = "Prob. ")|>
  mutate(alternative = factor(alternative, levels = c("adult", "non-hh", "alone")),
         has_big_sib = as.character(has_big_sib))

old_sib_plot_ind <- ggplot(vary_old_sib_preds_ind) +
  geom_bar(aes(x = has_big_sib, 
               y = value,
               fill = alternative),
           stat = "identity",
           position = position_stack(),
           alpha = 0.6) +
  scale_fill_manual(values = c("#7570B3",
                               "#D95F02",
                               "#1B9E77"),
                    labels = c("With parent",
                               "With others", 
                               "Alone"),
                    name = "Independence") +
  scale_x_discrete(name = "Has older sibling",
                   labels = c("No", "Yes")) +
  scale_y_continuous(name = "Probability") +
  theme_minimal() 

vary_lil_sib_preds_ind <- ind_data |>
  filter(income_k == 97.602533172497 & 
           (age > 10.15 & age < 10.2) &
           (veh_per_driver > 1.08 & veh_per_driver < 1.2) &
           (n_adults > 2.02 & n_adults < 2.08) &
           (distance > 1.087 & distance < 1.1) &
           (density > 2447 & density < 2563) &
           non_work_mom == 0 &
           non_work_dad == 0 &
           female == 0 &
           has_big_sib == 0) |>
  group_by(has_lil_sib) |>
  summarise(`Prob. adult` = mean(`Prob. adult`), 
            `Prob. non-hh` = mean(`Prob. non-hh`), 
            `Prob. alone` = mean(`Prob. alone`)) |>
  pivot_longer(cols = -has_lil_sib, names_to = "alternative", names_prefix = "Prob. ")|>
  mutate(alternative = factor(alternative, levels = c("adult", "non-hh", "alone")),
         has_lil_sib = as.character(has_lil_sib))

lil_sib_plot_ind <- ggplot(vary_lil_sib_preds_ind) +
  geom_bar(aes(x = has_lil_sib, 
               y = value,
               fill = alternative),
           stat = "identity",
           position = position_stack(),
           alpha = 0.6) +
  scale_fill_manual(values = c("#7570B3",
                               "#D95F02",
                               "#1B9E77"),
                    labels = c("With parent",
                               "With others",
                               "Alone"),
                    name = "Independence") +
  scale_x_discrete(name = "Has younger sibling",
                   labels = c("No", "Yes")) +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

vary_dist_preds_ind <- ind_data |>
  select(distance, `Prob. adult`, `Prob. non-hh`, `Prob. alone`) |>
  filter(distance <= 1.09 | distance >= 1.1) |>
  pivot_longer(cols = -distance, names_to = "alternative", names_prefix = "Prob. ") |>
  mutate(alternative = factor(alternative, levels = c("adult", "non-hh", "alone")))

dist_plot_ind <- ggplot(vary_dist_preds_ind) +
  geom_area(aes(x = distance, 
                y = value,
                fill = alternative),
            alpha = 0.6) +
  scale_fill_manual(values = c("#7570B3",
                               "#D95F02",
                               "#1B9E77"),
                    labels = c("With parent",
                               "With others",
                               "Alone"),
                    name = "Independence") +
  scale_x_continuous(name = "Trip distance (km)",
                     breaks = seq(0, 2, by=0.5),
                     labels = seq(0, 2, by = 0.5)) +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

vary_dens_preds_ind <- ind_data |>
  select(density, `Prob. adult`, `Prob. non-hh`, `Prob. alone`) |>
  filter(density <= 2447 | density >= 2563) |>
  pivot_longer(cols = -density, names_to = "alternative", names_prefix = "Prob. ") |>
  mutate(alternative = factor(alternative, levels = c("adult", "non-hh", "alone")))

dens_plot_ind <- ggplot(vary_dens_preds_ind) +
  geom_area(aes(x = density, 
                y = value,
                fill = alternative),
            alpha = 0.6) +
  scale_fill_manual(values = c("#7570B3",
                               "#D95F02",
                               "#1B9E77"),
                    labels = c("With parent",
                               "With others",
                               "Alone"),
                    name = "Independence") +
  scale_x_continuous(name = "Population density\n(people per square km)",
                     breaks = c(5000, 10000)) +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

non_work_mom_plot_ind + age_plot_ind + 
  female_plot_ind + old_sib_plot_ind +
  lil_sib_plot_ind + dist_plot_ind + dens_plot_ind +
  guide_area() + 
  plot_layout(guides = 'collect')

ggsave(filename = here("models",
                       "mode-ind-choice",
                       "trb-models",
                       "prob_plots_ind.png"), 
       width = 6.25, height = 6, units = "in", dpi = 300)

################## Combined

vary_dist_preds = nest_data |>
  select(distance, 
         `Prob. adult car`, 
         `Prob. non-hh car`, 
         `Prob. alone bike`,
         `Prob. adult bike`,
         `Prob. non-hh bike`,
         `Prob. alone walk`,
         `Prob. adult walk`,
         `Prob. non-hh walk`) |>
  filter(distance <= 1.09 | distance >= 1.1) |>
  pivot_longer(cols = -distance, names_to = "alternative", names_prefix = "Prob. ") |>
  mutate(alternative = factor(alternative, levels = c("adult car",
                                                      "adult bike",
                                                      "adult walk",
                                                      "non-hh car",
                                                      "non-hh bike",
                                                      "non-hh walk",
                                                      "alone bike", 
                                                      "alone walk")))

dist_plot <- ggplot(vary_dist_preds) +
  geom_area(aes(x = distance, 
                y = value,
                fill = alternative),
            alpha = 0.6) +
  scale_fill_manual(values = c("#58539d",
                               "#7570B3",
                               "#9491c5",
                               "#a84900",
                               "#D95F02",
                               "#ff770f",
                               "#1B9E77",
                               "#22c997"),
                    labels = c("Car with parent",
                               "Bike with parent",
                               "Walk with parent",
                               "Car with others",
                               "Bike with others",
                               "Walk with others",
                               "Bike alone",
                               "Walk alone"),
                    name = "Mode/Independence") +
  scale_x_continuous(name = "Trip distance (km)",
                     breaks = seq(0, 2, by=0.5),
                     labels = seq(0, 2, by = 0.5)) +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

vary_age_preds = nest_data |>
  select(age, 
         `Prob. adult car`, 
         `Prob. non-hh car`, 
         `Prob. alone bike`,
         `Prob. adult bike`,
         `Prob. non-hh bike`,
         `Prob. alone walk`,
         `Prob. adult walk`,
         `Prob. non-hh walk`) |>
  filter(age <= 10.15 | age >= 10.2) |>
  pivot_longer(cols = -age, names_to = "alternative", names_prefix = "Prob. ") |>
  mutate(alternative = factor(alternative, levels = c("adult car",
                                                      "adult bike",
                                                      "adult walk",
                                                      "non-hh car",
                                                      "non-hh bike",
                                                      "non-hh walk",
                                                      "alone bike", 
                                                      "alone walk")))

age_plot <- ggplot(vary_age_preds) +
  geom_area(aes(x = age, 
                y = value,
                fill = alternative),
            alpha = 0.6) +
  scale_fill_manual(values = c("#58539d",
                               "#7570B3",
                               "#9491c5",
                               "#a84900",
                               "#D95F02",
                               "#ff770f",
                               "#1B9E77",
                               "#22c997"),
                    labels = c("Car with parent",
                               "Bike with parent",
                               "Walk with parent",
                               "Car with others",
                               "Bike with others",
                               "Walk with others",
                               "Bike alone",
                               "Walk alone"),
                    name = "Mode/Independence") +
  scale_x_continuous(name = "Age") +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

vary_dens_preds = nest_data |>
  select(density, 
         `Prob. adult car`, 
         `Prob. non-hh car`, 
         `Prob. alone bike`,
         `Prob. adult bike`,
         `Prob. non-hh bike`,
         `Prob. alone walk`,
         `Prob. adult walk`,
         `Prob. non-hh walk`) |>
  filter(density <= 2447 | density >= 2563) |>
  pivot_longer(cols = -density, names_to = "alternative", names_prefix = "Prob. ") |>
  mutate(alternative = factor(alternative, levels = c("adult car",
                                                      "adult bike",
                                                      "adult walk",
                                                      "non-hh car",
                                                      "non-hh bike",
                                                      "non-hh walk",
                                                      "alone bike", 
                                                      "alone walk")))


dens_plot <- ggplot(vary_dens_preds) +
  geom_area(aes(x = density, 
                y = value,
                fill = alternative),
            alpha = 0.6) +
  scale_fill_manual(values = c("#58539d",
                               "#7570B3",
                               "#9491c5",
                               "#a84900",
                               "#D95F02",
                               "#ff770f",
                               "#1B9E77",
                               "#22c997"),
                    labels = c("Car with parent",
                               "Bike with parent",
                               "Walk with parent",
                               "Car with others",
                               "Bike with others",
                               "Walk with others",
                               "Bike alone",
                               "Walk alone"),
                    name = "Mode/Independence") +
  scale_x_continuous(name = "Population density\n(people per square km)",
                     breaks = c(5000, 10000),
                     labels = c("5 000", "10 000")) +
  scale_y_continuous(name = "Probability") +
  theme_minimal()

vary_non_work_mom_preds <- nest_data |>
  filter(income_k == 97.602533172497 & 
           (age > 10.15 & age < 10.2) &
           (veh_per_driver > 1.08 & veh_per_driver < 1.2) &
           (n_adults > 2.02 & n_adults < 2.08) &
           (distance > 1.087 & distance < 1.1) &
           (density > 2447 & density < 2563) &
           female == 0 &
           non_work_dad == 0 &
           has_big_sib == 0 &
           has_lil_sib == 0) |>
  group_by(non_work_mom) |>
  summarise(`Prob. adult car` = mean(`Prob. adult car`),
            `Prob. adult bike` = mean(`Prob. adult bike`),
            `Prob. adult walk` = mean(`Prob. adult walk`),
            `Prob. non-hh car` = mean(`Prob. non-hh car`),
            `Prob. non-hh bike` = mean(`Prob. non-hh bike`),
            `Prob. non-hh walk` = mean(`Prob. non-hh walk`),
            `Prob. alone bike` = mean(`Prob. alone bike`),
            `Prob. alone walk` = mean(`Prob. alone walk`)) |>
  pivot_longer(cols = -non_work_mom, names_to = "alternative", names_prefix = "Prob. ")|>
  mutate(alternative = factor(alternative, levels = c("adult car",
                                                      "adult bike",
                                                      "adult walk",
                                                      "non-hh car",
                                                      "non-hh bike",
                                                      "non-hh walk",
                                                      "alone bike", 
                                                      "alone walk")),
         non_work_mom = as.character(non_work_mom))

non_work_mom_plot <- ggplot(vary_non_work_mom_preds) +
  geom_bar(aes(x = non_work_mom, 
               y = value,
               fill = alternative),
           stat = "identity",
           position = position_stack(),
           alpha = 0.6) +
  scale_fill_manual(values = c("#58539d",
                               "#7570B3",
                               "#9491c5",
                               "#a84900",
                               "#D95F02",
                               "#ff770f",
                               "#1B9E77",
                               "#22c997"),
                    labels = c("Car with parent",
                               "Bike with parent",
                               "Walk with parent",
                               "Car with others",
                               "Bike with others",
                               "Walk with others",
                               "Bike alone",
                               "Walk alone"),
                    name = "Mode/Independence") +
  scale_x_discrete(name = "Non-working mother",
                   labels = c("No",
                              "Yes")) +
  scale_y_continuous(name = "Probability") +
  theme_minimal() 

vary_female_preds <- nest_data |>
  filter(income_k == 97.602533172497 & 
           (age > 10.15 & age < 10.2) &
           (veh_per_driver > 1.08 & veh_per_driver < 1.2) &
           (n_adults > 2.02 & n_adults < 2.08) &
           (distance > 1.087 & distance < 1.1) &
           (density > 2447 & density < 2563) &
           non_work_mom == 0 &
           non_work_dad == 0 &
           has_big_sib == 0 &
           has_lil_sib == 0) |>
  group_by(female) |>
  summarise(`Prob. adult car` = mean(`Prob. adult car`),
            `Prob. adult bike` = mean(`Prob. adult bike`),
            `Prob. adult walk` = mean(`Prob. adult walk`),
            `Prob. non-hh car` = mean(`Prob. non-hh car`),
            `Prob. non-hh bike` = mean(`Prob. non-hh bike`),
            `Prob. non-hh walk` = mean(`Prob. non-hh walk`),
            `Prob. alone bike` = mean(`Prob. alone bike`),
            `Prob. alone walk` = mean(`Prob. alone walk`)) |>
  pivot_longer(cols = -female, names_to = "alternative", names_prefix = "Prob. ")|>
  mutate(alternative = factor(alternative, levels = c("adult car",
                                                      "adult bike",
                                                      "adult walk",
                                                      "non-hh car",
                                                      "non-hh bike",
                                                      "non-hh walk",
                                                      "alone bike", 
                                                      "alone walk")),
         female = as.character(female))

female_plot <- ggplot(vary_female_preds) +
  geom_bar(aes(x = female, 
               y = value,
               fill = alternative),
           stat = "identity",
           position = position_stack(),
           alpha = 0.6) +
  scale_fill_manual(values = c("#58539d",
                               "#7570B3",
                               "#9491c5",
                               "#a84900",
                               "#D95F02",
                               "#ff770f",
                               "#1B9E77",
                               "#22c997"),
                    labels = c("Car with parent",
                               "Bike with parent",
                               "Walk with parent",
                               "Car with others",
                               "Bike with others",
                               "Walk with others",
                               "Bike alone",
                               "Walk alone"),
                    name = "Mode/Independence") +
  scale_x_discrete(name = "Gender",
                   labels = c("Boys", "Girls")) +
  scale_y_continuous(name = "Probability") +
  theme_minimal() 

lil_sib_plot <- ggplot(vary_lil_sib_preds) +
  geom_bar(aes(x = has_lil_sib, 
               y = probability,
               fill = alternative),
           stat = "identity",
           position = position_stack(),
           alpha = 0.6) +
  scale_fill_manual(values = c("#58539d",
                               "#7570B3",
                               "#9491c5",
                               "#a84900",
                               "#D95F02",
                               "#ff770f",
                               "#1B9E77",
                               "#22c997"),
                    labels = c("Car with household\nadult",
                               "Bike with household\nadult",
                               "Walk with household\nadult",
                               "Car with others",
                               "Bike with others",
                               "Walk with others",
                               "Bike alone",
                               "Walk alone"),
                    name = "Mode/Independence") +
  scale_x_discrete(name = "Has younger sibling",
                   labels = c("No", "Yes")) +
  scale_y_continuous(name = "Probability") +
  theme_minimal() 

old_sib_plot <- ggplot(vary_old_sib_preds) +
  geom_bar(aes(x = has_old_sib, 
               y = probability,
               fill = alternative),
           stat = "identity",
           position = position_stack(),
           alpha = 0.6) +
  scale_fill_manual(values = c("#58539d",
                               "#7570B3",
                               "#9491c5",
                               "#a84900",
                               "#D95F02",
                               "#ff770f",
                               "#1B9E77",
                               "#22c997"),
                    labels = c("Car with household\nadult",
                               "Bike with household\nadult",
                               "Walk with household\nadult",
                               "Car with others",
                               "Bike with others",
                               "Walk with others",
                               "Bike alone",
                               "Walk alone"),
                    name = "Mode/Independence") +
  scale_x_discrete(name = "Has older sibling",
                   labels = c("No", "Yes")) +
  scale_y_continuous(name = "Probability") +
  theme_minimal() 