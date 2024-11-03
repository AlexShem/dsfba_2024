library(methods)
library(tidyverse)
library(knitr)
set.seed(1014)

# options(lifecycle_warnings_as_errors = TRUE)

knitr::opts_chunk$set(
  comment = "#>",
  collapse = TRUE,
  size = "footnotesize",
  #cache = TRUE,
  fig.retina = 0.8, # figures are either vectors or 300 dpi diagrams
  dpi = 300,
  out.width = "70%",
  fig.align = 'center',
  fig.width = 6,
  fig.asp = 0.618,  # 1 / phi
  fig.show = "hold"
)

# ## On my laptop
# knitr::opts_chunk$set(width = 69)
# chunk_hook  <- knit_hooks$get("chunk")
# knit_hooks$set(chunk = function(x, options) {
#   x <- chunk_hook(x, options)
#   ifelse(options$size != "normalsize",
#          paste0("\\vspace{-0.4cm} \\", options$size,"\n\n", x, "\n \\vspace{-0.7cm} \\normalsize"), x)
# })

## On my desktop computer
knitr::opts_chunk$set(width = 69)
chunk_hook  <- knit_hooks$get("chunk")
knit_hooks$set(chunk = function(x, options) {
  x <- chunk_hook(x, options)
  ifelse(options$size != "normalsize",
         paste0("\\vspace{0.1cm} \\", options$size,"\n\n", x, "\n \\vspace{-0.2cm} \\normalsize"), x)
})

# knitr::knit_hooks$set(
#   small_mar = function(before, options, envir) {
#     if (before) {
#       par(mar = c(4.1, 4.1, 0.5, 0.5))
#     }
#   }
# )

theme_set(theme_light(base_size = 18))

options(
  digits = 5,
  str = strOptions(strict.width = "cut"),
  width = 69,
  tibble.width = 69,
  # crayon.enabled = TRUE,
  cli.unicode = FALSE
)


# # Make error messages closer to base R
# registerS3method("wrap", "error", envir = asNamespace("knitr"),
#                  function(x, options) {
#                    msg <- conditionMessage(x)
#
#                    call <- conditionCall(x)
#                    if (is.null(call)) {
#                      msg <- paste0("Error: ", msg)
#                    } else {
#                      msg <- paste0("Error in ", deparse(call)[[1]], ": ", msg)
#                    }
#                    msg <- error_wrap(msg)
#                    knitr:::msg_wrap(msg, "error", options)
#                  }
# )

error_wrap <- function(x, width = getOption("width")) {
  lines <- strsplit(x, "\n", fixed = TRUE)[[1]]
  paste(strwrap(lines, width = width), collapse = "\n")
}
#
# wrap.simpleError <- function(x, width = NULL) {
#   width <- getOption("width")
#   # # x is an error object, with components "call" and "message".  Ignore
#   # # the call, but wrap the result like code:
#   # paste0("```\n## Error: ", x$message, "\n```")
#   browser()
#   msg <- paste0("Error in ", capture.output(x$call), ": ", x$message)
#   paste("```\n#> ", str_wrap(msg, width = width), "\n```", collapse = "")
# }
