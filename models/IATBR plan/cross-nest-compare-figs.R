library(tidyverse)

## It would be better not to have to type these in manually, like if I had
## output them to a csv file from biogeme instead of just the html summary.
## Oh Well.

var_names <- c("intercept",
               "Year 2017 (relative to 2009)",
               "log(household income)",
               "Vehicles per driver",
               "Non-working father",
               "Non-working mother",
               "Age",
               "Female",
               "Has younger sibling",
               "Has older sibling",
               "log(trip distance)",
               "log(density)")

var_names <- factor(var_names, levels = var_names)

results <- tibble(model = c(rep("Cross-nested", 24), 
                                       rep("Unnested", 24)),
                             variable= rep(sort(rep(var_names, 2)), 2),
                  alternative= rep(rep(c("Utility of traveling WITHOUT\na parent by active modes\n(relative to traveling by car)",
                                         "Utility of traveling WITH\na parent by active modes\n(relative to traveling by car)"),12), 2),
                             coeff = c(-4.91,
                                       -3.85,
                                       0.08,
                                       1.26,
                                       -0.04,
                                       0.01,
                                       -0.25,
                                       -0.53,
                                       -0.06,
                                       0.06,
                                       -0.09,
                                       0.16,
                                       0.21,
                                       -0.05,
                                       -0.29,
                                       -0.14,
                                       0.19,
                                       0.2,
                                       0.32,
                                       0.08,
                                       -1.52,
                                       -1.27,
                                       0.18,
                                       0.25,
                                       -5.22,
                                       -5.68,
                                       -0.2,
                                       2.7,
                                       -0.05,
                                       0.07,
                                       -0.19,
                                       -1.13,
                                       -0.11,
                                       0.2,
                                       -0.12,
                                       0.42,
                                       0.24,
                                       -0.25,
                                       -0.32,
                                       -0.13,
                                       0.21,
                                       0.29,
                                       0.34,
                                       0.04,
                                       -1.63,
                                       -1.73,
                                       0.17,
                                       0.4),
                             se = c(0.37,
                                    0.68,
                                    0.12,
                                    0.14,
                                    0.04,
                                    0.05,
                                    0.09,
                                    0.12,
                                    0.10,
                                    0.12,
                                    0.07,
                                    0.08,
                                    0.02,
                                    0.03,
                                    0.07,
                                    0.08,
                                    0.07,
                                    0.08,
                                    0.07,
                                    0.08,
                                    0.08,
                                    0.22,
                                    0.03,
                                    0.04,
                                    0.4,
                                    0.9,
                                    0.07,
                                    0.19,
                                    0.04,
                                    0.07,
                                    0.09,
                                    0.23,
                                    0.12,
                                    0.19,
                                    0.08,
                                    0.14,
                                    0.02,
                                    0.04,
                                    0.07,
                                    0.13,
                                    0.08,
                                    0.14,
                                    0.08,
                                    0.14,
                                    0.06,
                                    0.11,
                                    0.03,
                                    0.08)) 

results <- results |>
  mutate(low = coeff - 1.96*se,
         hi = coeff + 1.96*se) 

results_no_int <- results |>
  filter(variable != "intercept")

ggplot(results_no_int, aes(x=variable, y=coeff, group=model, color=model)) + 
  geom_point(position=position_dodge(0.5), shape = "+", size = 2)+
  geom_errorbar(aes(ymin=low, ymax=hi), width=0.5,
                position=position_dodge(0.5)) +
  scale_y_continuous(name = "Coefficient estimate\n(with 95-percent confidence interval)") +
  scale_x_discrete(name = "Variable") +
  scale_color_manual(name = "Model nesting\nstructure",
                       values = c("black", "gray50")) +
  geom_hline(yintercept = 0, lty = "dotted", size = 0.5) +
  facet_wrap("alternative") +
#  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

ggsave("compare_nests.png", dpi = 600, width = 6, height = 6, units = "in")
