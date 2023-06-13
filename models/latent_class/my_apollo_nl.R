apollo_nl <- function (nl_settings, functionality) {
  modelType = "NL"
  if (is.null(nl_settings[["componentName"]])) {
    nl_settings[["componentName"]] = ifelse(!is.null(nl_settings[["componentName2"]]), 
                                            nl_settings[["componentName2"]], modelType)
    test <- functionality == "validate" && nl_settings[["componentName"]] != 
      "model" && !apollo_inputs$silent
    if (test) 
      apollo_print(paste0("Apollo found a model component of type ", 
                          modelType, " without a componentName. The name was set to \"", 
                          nl_settings[["componentName"]], "\" by default."))
  }
  if (functionality == "validate") {
    apollo_modelList <- tryCatch(get("apollo_modelList", 
                                     envir = parent.frame(), inherits = FALSE), error = function(e) c())
    apollo_modelList <- c(apollo_modelList, nl_settings$componentName)
    if (anyDuplicated(apollo_modelList)) 
      stop("SPECIFICATION ISSUE - Duplicated componentName found (", 
           nl_settings$componentName, "). Names must be different for each component.")
    assign("apollo_modelList", apollo_modelList, envir = parent.frame())
  }
  if (!is.null(nl_settings[["utilities"]])) 
    names(nl_settings)[which(names(nl_settings) == "utilities")] = "V"
  apollo_inputs = tryCatch(get("apollo_inputs", parent.frame(), 
                               inherits = FALSE), error = function(e) return(list(apollo_control = list(cpp = FALSE))))
  if (!is.null(apollo_inputs[[paste0(nl_settings$componentName, 
                                     "_settings")]]) && (functionality != "preprocess")) {
    tmp <- apollo_inputs[[paste0(nl_settings$componentName, 
                                 "_settings")]]
    if (is.null(tmp$V)) 
      tmp$V <- nl_settings$V
    if (is.null(tmp$nlNests)) 
      tmp$nlNests <- nl_settings$nlNests
    if (is.null(tmp$nlStructure)) 
      tmp$nlStructure <- nl_settings$nlStructure
    nl_settings <- tmp
    rm(tmp)
  } else {
    nl_settings <- apollo_preprocess(inputs = nl_settings, 
                                     modelType, functionality, apollo_inputs)
    if (apollo_inputs$apollo_control$cpp) 
      if (!apollo_inputs$silent) 
        apollo_print("No C++ optimisation available for NL")
    nl_settings$probs_NL <- function(nl_settings, all = FALSE) {
      nl_settings$choiceNA = FALSE
      if (all(is.na(nl_settings$choiceVar))) {
        nl_settings$choiceVar = nl_settings$alternatives[1]
        nl_settings$choiceNA = TRUE
      }
      nl_settings$V <- mapply(function(v, a) apollo_setRows(v, 
                                                            !a, 0), nl_settings$V, nl_settings$avail, SIMPLIFY = FALSE)
      if (!all) 
        VSubs <- Reduce("+", mapply("*", nl_settings$Y, 
                                    nl_settings$V, SIMPLIFY = FALSE))
      else VSubs <- do.call(pmax, nl_settings$V)
      nl_settings$V <- lapply(nl_settings$V, "-", VSubs)
      rm(VSubs)
      for (k in length(nl_settings$nlStructure):1) {
        nestK <- names(nl_settings$nlStructure)[k]
        nl_settings$V[[nestK]] = 0
        nl_settings$avail[[nestK]] = 1 * (Reduce("+", 
                                                 nl_settings$avail[nl_settings$nlStructure[[k]]]) > 
                                            0)
        for (j in 1:length(nl_settings$nlStructure[[k]])) {
          nodeJ <- nl_settings$nlStructure[[k]][j]
          nl_settings$V[[nestK]] = nl_settings$V[[nestK]] + 
            nl_settings$avail[[nodeJ]] * exp(nl_settings$V[[nodeJ]]/nl_settings$nlNests[[nestK]])
        }
        nl_settings$V[[nestK]] = nl_settings$nlNests[[nestK]] * 
          log(nl_settings$V[[nestK]])
      }
      logPalts = list()
      for (j in 1:length(nl_settings$altnames)) {
        logPalts[[j]] = 0
        ancestorsJ <- nl_settings$ancestors[[nl_settings$altnames[[j]]]]
        for (k in 1:(length(ancestorsJ) - 1)) {
          current_V = nl_settings$V[[ancestorsJ[k]]]
          next_V = nl_settings$V[[ancestorsJ[k + 1]]]
          logPalts[[j]] = logPalts[[j]] + (current_V - 
                                             next_V)/nl_settings$nlNests[[ancestorsJ[k + 
                                                                                       1]]]
        }
      }
      Palts = lapply(X = logPalts, FUN = exp)
      names(Palts) = names(nl_settings$V)[1:length(nl_settings$altnames)]
      Palts <- mapply("*", Palts, nl_settings$avail[1:length(nl_settings$altnames)], 
                      SIMPLIFY = FALSE)
      Palts <- lapply(Palts, function(x) {
        x[is.na(x)] <- 0
        return(x)
      })
      if (!(all && nl_settings$choiceNA)) 
        Palts[["chosen"]] <- Reduce("+", mapply("*", 
                                                nl_settings$Y, Palts, SIMPLIFY = FALSE))
      if (!all) 
        Palts <- Palts[["chosen"]]
      return(Palts)
    }
    nl_settings$nl_diagnostics <- function(inputs, apollo_inputs, 
                                           data = TRUE, param = TRUE) {
      for (i in 1:length(inputs$avail)) if (length(inputs$avail[[i]]) == 
                                            1) 
        inputs$avail[[i]] <- rep(inputs$avail[[i]], inputs$nObs)
      choicematrix = matrix(0, nrow = 4, ncol = length(inputs$altnames), 
                            dimnames = list(c("Times available", "Times chosen", 
                                              "Percentage chosen overall", "Percentage chosen when available"), 
                                            inputs$altnames))
      choicematrix[1, ] = unlist(lapply(inputs$avail, sum))
      for (j in 1:length(inputs$altnames)) choicematrix[2, 
                                                        j] = sum(inputs$choiceVar == inputs$altcodes[j])
      choicematrix[3, ] = choicematrix[2, ]/inputs$nObs * 
        100
      choicematrix[4, ] = choicematrix[2, ]/choicematrix[1, 
      ] * 100
      choicematrix[4, !is.finite(choicematrix[4, ])] <- 0
      if (!apollo_inputs$silent & data) {
        if (any(choicematrix[4, ] == 0)) 
          apollo_print("Some alternatives are never chosen in your data!", 
                       type = "w")
        if (any(choicematrix[4, ] >= 100)) 
          apollo_print("Some alternatives are always chosen when available!", 
                       type = "w")
        apollo_print("\n")
        apollo_print(paste0("Overview of choices for ", 
                            toupper(inputs$modelType), " model component ", 
                            ifelse(inputs$componentName == "model", "", 
                                   inputs$componentName), ":"))
        print(round(choicematrix, 2))
      }
      if (param) {
        if (!apollo_inputs$silent & data) 
          apollo_print("\n")
        if (!apollo_inputs$silent) {
          if (inputs$root_set) 
            apollo_print("Notice: Root lambda parameter set to 1.")
          nestAbove <- unique(lapply(inputs$ancestors, 
                                     "[", -1))
          nestAbove <- setNames(sapply(nestAbove, function(x) if (length(x) == 
                                                                  1) 
            return("Inf")
            else x[2]), sapply(nestAbove, "[", 1))
          apollo_print(paste0("Nesting structure for ", 
                              toupper(inputs$modeltype), " model component ", 
                              ifelse(inputs$componentName == "model", "", 
                                     inputs$componentName), ":"))
          print_tree_level = function(nlStructure, component, 
                                      preceding_nest_layer, space) {
            if (preceding_nest_layer != 0) 
              space = c(space, "  |")
            for (j in 1:length(nlStructure[[component]])) {
              space <- gsub("[']", " ", space)
              if (j == length(nlStructure[[component]])) 
                space[length(space)] <- gsub("[|]", "'", 
                                             space[length(space)])
              if (nlStructure[[component]][j] %in% inputs$altnames) {
                depth <- length(space)
                cat("\n", space, rep("-", 3 * (maxDepth - 
                                                 depth)), "-Alternative: ", nlStructure[[component]][j], 
                    sep = "")
              }
              else {
                l <- inputs$nlNests[[nlStructure[[component]][j]]]
                if (length(l) > 1) {
                  cat("\n", space, "-Nest: ", nlStructure[[component]][j], 
                      " (distributed, mean: ", mean(l), 
                      ")", sep = "")
                }
                else {
                  cat("\n", space, "-Nest: ", nlStructure[[component]][j], 
                      " (", round(l, 4), ")", sep = "")
                }
                print_tree_level(nlStructure, nlStructure[[component]][j], 
                                 preceding_nest_layer + 1, space)
              }
            }
          }
          maxDepth <- max(sapply(inputs$ancestors, length)) - 
            1
          cat("Nest: ", names(inputs$nlStructure)[[1]], 
              " (", round(inputs$nlNests[[names(inputs$nlStructure)[[1]]]], 
                          4), ")", sep = "")
          print_tree_level(inputs$nlStructure, "root", 
                           preceding_nest_layer = 0, space = "|")
          apollo_print("\n")
          for (i in names(inputs$nlNests)) {
            l <- inputs$nlNests[[i]]
            if (i == "root") 
              l0 <- 1
            else l0 <- inputs$nlNests[[nestAbove[i]]]
            if (length(l) == 1 && any(l < 0 | l0 < l)) {
              txt <- paste0("The nesting parameter for nest \"", 
                            i, "\" should be between 0 and ", round(l0, 
                                                                    4))
              if (i != "root") 
                txt <- paste0(txt, " (the nesting parameter for nest \"", 
                              nestAbove[i], "\")")
              txt <- paste0(txt, ", yet its value is ", 
                            round(l, 4), ".")
              cat("\n")
              apollo_print(txt, type = "w")
            }
          }
        }
      }
      return(invisible(TRUE))
    }
    nl_settings$modelType <- modelType
    apollo_beta <- tryCatch(get("apollo_beta", envir = parent.frame(), 
                                inherits = TRUE), error = function(e) return(NULL))
    test <- !is.null(apollo_beta) && functionality %in% c("preprocess", 
                                                          "gradient")
    test <- test && all(sapply(nl_settings$V, is.function))
    test <- test && apollo_inputs$apollo_control$analyticGrad
    nl_settings$gradient <- FALSE
    if (test) {
      nl_settings$dV <- apollo_dVdB(apollo_beta, apollo_inputs, 
                                    nl_settings$V)
      nl_settings$gradient <- !is.null(nl_settings$dV)
    }
    rm(test)
    if (functionality == "preprocess") {
      nl_settings$V <- NULL
      nl_settings$nlNests <- NULL
      nl_settings$nlStructure <- NULL
      return(nl_settings)
    }
  }
  if (any(sapply(nl_settings$V, is.function))) {
    nl_settings$V = lapply(nl_settings$V, function(f) if (is.function(f)) 
      f()
      else f)
  }
  if (any(sapply(nl_settings$nlNests, is.function))) {
    nl_settings$nlNests = lapply(nl_settings$nlNests, function(f) if (is.function(f)) 
      f()
      else f)
  }
  if (is.function(nl_settings$nlStructure)) 
    nl_settings$nlStructure <- nl_settings$nlStructure()
  nl_settings$V <- lapply(nl_settings$V, function(v) if (is.matrix(v) && 
                                                         ncol(v) == 1) 
    as.vector(v)
    else v)
  nl_settings$V <- nl_settings$V[nl_settings$altnames]
  if (!all(nl_settings$rows)) 
    nl_settings$V <- lapply(nl_settings$V, apollo_keepRows, 
                            r = nl_settings$rows)
  if (functionality == "validate") {
    if (!apollo_inputs$apollo_control$noValidation) 
      apollo_validate(nl_settings, modelType, functionality, 
                      apollo_inputs)
    if (!apollo_inputs$apollo_control$noDiagnostics) 
      nl_settings$nl_diagnostics(nl_settings, apollo_inputs)
    testL = nl_settings$probs_NL(nl_settings)
    if (any(!nl_settings$rows)) 
      testL <- apollo_insertRows(testL, nl_settings$rows, 
                                 1)
    if (all(testL == 0)) 
      stop("CALCULATION ISSUE - All observations have zero probability at starting value for model component \"", 
           nl_settings$componentName, "\"")
    if (any(testL == 0) && !apollo_inputs$silent && apollo_inputs$apollo_control$debug) 
      apollo_print(paste0("Some observations have zero probability at starting value for model component \"", 
                          nl_settings$componentName, "\""), type = "i")
    return(invisible(testL))
  }
  if (functionality == "zero_LL") {
    for (i in 1:nl_settings$nAlt) if (length(nl_settings$avail[[i]]) == 
                                      1) 
      nl_settings$avail[[i]] <- rep(nl_settings$avail[[i]], 
                                    nl_settings$nObs)
    nAvAlt <- rowSums(matrix(unlist(nl_settings$avail), ncol = nl_settings$nAlt))
    P = 1/nAvAlt
    if (any(!nl_settings$rows)) 
      P <- apollo_insertRows(P, nl_settings$rows, 1)
    return(P)
  }
  if (functionality == "shares_LL") {
    for (i in 1:length(nl_settings$avail)) if (length(nl_settings$avail[[i]]) == 
                                               1) 
      nl_settings$avail[[i]] <- rep(nl_settings$avail[[i]], 
                                    nl_settings$nObs)
    nAvAlt <- rowSums(do.call(cbind, nl_settings$avail))
    Y = do.call(cbind, nl_settings$Y)
    if (var(nAvAlt) == 0) {
      Yshares = colSums(Y)/nrow(Y)
      P = as.vector(Y %*% Yshares)
    }
    else {
      mnl_ll = function(b, A, Y) as.vector(Y %*% c(b, 0) - 
                                             log(rowSums(A %*% exp(c(b, 0)))))
      A = do.call(cbind, nl_settings$avail)
      b = maxLik::maxLik(mnl_ll, start = rep(0, nl_settings$nAlt - 
                                               1), method = "BFGS", finalHessian = FALSE, A = A, 
                         Y = Y)$estimate
      P = exp(mnl_ll(b, A, Y))
    }
    if (any(!nl_settings$rows)) 
      P <- apollo_insertRows(P, nl_settings$rows, 1)
    return(P)
  }
  if (functionality %in% c("estimate", "conditionals", "output", 
                           "components")) {
    P <- nl_settings$probs_NL(nl_settings, all = FALSE)
    if (any(!nl_settings$rows)) 
      P <- apollo_insertRows(P, nl_settings$rows, 1)
    return(P)
  }
  if (functionality %in% c("prediction", "raw")) {
    P <- nl_settings$probs_NL(nl_settings, all = TRUE)
    if (any(!nl_settings$rows)) 
      P <- lapply(P, apollo_insertRows, r = nl_settings$rows, 
                  val = NA)
    return(P)
  }
  if (functionality == "report") {
    P <- list()
    apollo_inputs$silent <- FALSE
    P$data <- capture.output(nl_settings$nl_diagnostics(nl_settings, 
                                                        apollo_inputs, param = FALSE))
    P$param <- capture.output(nl_settings$nl_diagnostics(nl_settings, 
                                                         apollo_inputs, data = FALSE))
    return(P)
  }
}
