# Advanced Data Manipulation and Modeling with `tidyverse` in R

## Table of Contents

1. **Introduction to Tidy Evaluation in `dplyr`**
   - Overview of `dplyr`’s use of tidy evaluation, enabling more concise and expressive code when working with data variables.

2. **Data Masking in `dplyr`**
   - Explanation of data masking to simplify data manipulation by directly referencing column names without the `$` prefix.

3. **Tidy Selection for Column Operations**
   - Overview of tidy selection functions like `select()`, `mutate()`, and `across()` to simplify column-based transformations based on criteria such as column type or name patterns.

4. **Programming with `dplyr`: Indirection Techniques**
   - Techniques for dynamic programming with `dplyr`, including `{{ }}`, `.data` pronoun, and `all_of()` for handling column names stored as variables in functions or loops.

5. **Building Custom Summarization Functions**
   - Step-by-step creation of flexible summarization functions that allow user-defined expressions and support multiple columns using `across()` and `summarise()`.

6. **Name Injection in Variable Names**
   - Demonstrate dynamic naming within pipelines using `:=` for customized output column names based on input expressions or environment variables.

7. **Creating and Using Nested Data Frames**
   - Introduction to nested data frames for grouped analyses, created via `tidyr::nest()`, and methods for managing and working with these nested structures.

8. **Building Models with Nested Data**
   - Guide to constructing models for each group within nested data, utilizing `purrr::map()` for fitting and `broom::tidy()` for collecting model results in tidy format.

9. **Applying `broom` for Model Summaries**
   - Using the `broom` package to transform model objects into tidy data frames, facilitating summaries, visualizations, and aggregations of modeling results.

10. **Integrating Modeling with EDA: Nest-Map-Unnest Workflow**
    - Comprehensive overview of the nest-map-unnest pattern for efficiently performing and summarizing models or analyses over multiple subgroups within data.

11. **Advanced Applications: Multi-Level Modeling and Result Aggregation**
    - Techniques for integrating more complex models, such as regressions with multiple predictors, and methods to handle augment, glance, and tidy outputs for advanced analysis across subgroups.

Here's the Quarto slide structure in Markdown format for sections 1-7. Each section includes theory followed by practical examples, organized into 2-4 slides per section.

---

# Introduction to Tidy Evaluation in `dplyr`

## What is Tidy Evaluation?
- **Tidy Evaluation** is a form of non-standard evaluation used in the `tidyverse`.
- It allows simpler expressions for data manipulation, making code more concise and readable.
- Two main concepts: **Data Masking** and **Tidy Selection**.

---

## Why Use Tidy Evaluation?
- Reduces the need for `df$column` syntax; instead, use `column` directly.
- Enables smooth data exploration and efficient manipulation, especially in interactive analysis.
- Supports consistent and flexible workflows across multiple `dplyr` functions.

---

## Practical Example: Tidy Evaluation
```r
# Filtering without Tidy Evaluation
starwars[starwars$homeworld == "Naboo" & starwars$species == "Human", ]

# Filtering with Tidy Evaluation
starwars %>% filter(homeworld == "Naboo", species == "Human")
```

---

# Data Masking in `dplyr`

## Overview of Data Masking
- **Data Masking** allows using data frame columns as if they were variables in the environment.
- Avoids repetitive references to the data frame.
- Key for efficient filtering, summarizing, and mutating.

---

## Data Masking in Action
- Distinguishes between **env-variables** (programming variables) and **data-variables** (statistical variables).
- Env-variables are created with `<-`, while data-variables are within the data frame.

---

## Practical Example: Data Masking
```r
# Using env-variable and data-variables
df <- data.frame(x = runif(3), y = runif(3))
df %>% mutate(z = x + y)
```

```r
# Filtering with Data Masking
starwars %>% filter(homeworld == "Naboo" & species == "Human")
```

---

# Tidy Selection for Column Operations

## What is Tidy Selection?
- **Tidy Selection** is a set of tools to easily select columns by name, type, or position.
- Allows for selecting columns dynamically within functions like `select()`, `mutate()`, `across()`.

---

## Tidy Selection Syntax
- Examples: `starts_with("x")`, `ends_with("z")`, `where(is.numeric)`.
- Can specify columns using multiple criteria within a single function.

---

## Practical Example: Tidy Selection
```r
# Selecting columns by pattern
mtcars %>% select(starts_with("c"))

# Selecting all numeric columns
mtcars %>% select(where(is.numeric))
```

---

# Programming with `dplyr`: Indirection Techniques

## What is Indirection in `dplyr`?
- **Indirection** refers to using variables dynamically within `dplyr` functions.
- Useful in functions and loops, especially when column names are stored as strings or variables.

---

## Techniques for Indirection
- Use `{{ }}` to embrace expressions within function arguments.
- `.data[[ ]]` helps when column names are in character vectors.

---

## Practical Example: Indirection with Embracing
```r
# Embracing with {{ }}
var_summary <- function(data, var) {
  data %>% summarise(n = n(), min = min({{ var }}), max = max({{ var }}))
}
mtcars %>% group_by(cyl) %>% var_summary(mpg)
```

```r
# Using .data with character vectors
vars <- c("mpg", "vs")
mtcars %>% summarise(across(all_of(vars), mean))
```

---

# Building Custom Summarization Functions

## Writing Flexible Summarization Functions
- Functions can accept variable column expressions to compute summaries dynamically.
- `across()` is key for creating flexible summaries over multiple columns.

---

## Custom Summarization Syntax
- Use `across()` inside `summarise()` to calculate statistics on chosen columns.
- Control output column names using `.names` within `across()`.

---

## Practical Example: Custom Summarization
```r
# Function to calculate means of selected columns
summarise_mean <- function(data, vars) {
  data %>% summarise(n = n(), across({{ vars }}, mean))
}
mtcars %>% group_by(cyl) %>% summarise_mean(where(is.numeric))
```

---

# Name Injection in Variable Names

## Dynamic Name Creation with Name Injection
- `:=` allows creating dynamic names for variables in a pipeline.
- Useful when column names are generated programmatically or from environment variables.

---

## Practical Example: Name Injection
```r
# Dynamic name assignment
name <- "dynamic_var"
tibble("{name}" := 2)

# Using dynamic name within a function
my_df <- function(x) {
  tibble("{{ x }}_2" := x * 2)
}
my_var <- 10
my_df(my_var)
```

---

# Creating and Using Nested Data Frames

## Introduction to Nested Data Frames
- **Nested Data Frames** are data frames with columns that are lists of data frames.
- Useful for working with grouped data and multiple models or transformations.

---

## Practical Example: Nesting and Unnesting
```r
# Creating nested data by group
df <- tibble(g = c(1, 2, 3), x = 1:3, y = 3:1)
nested_df <- df %>% group_by(g) %>% nest()

# Unnesting data
nested_df %>% unnest(data)
```



---



# Creating and Using Nested Data Frames

## What is a Nested Data Frame?
- A **Nested Data Frame** contains one or more columns as lists of data frames.
- Useful for organizing grouped data or subsetting for complex transformations and modeling.

---

## Creating Nested Data Frames
- Use `tidyr::nest()` to group columns into list-columns.
- Each list entry represents a data subset, allowing efficient grouping and nested operations.

```r
# Creating a nested data frame by grouping
df <- tribble(
  ~g, ~x, ~y,
   1,  1,  2,
   2,  4,  6,
   2,  5,  7,
   3, 10,  NA
)
df %>% nest(data = c(x, y))
```

---

## Practical Example: Nesting and Unnesting
```r
# Nesting by group
df_nested <- df %>% group_by(g) %>% nest()

# Unnesting to return original structure
df_nested %>% unnest(data)
```

---

# Nested Data and Modeling

## Using Nested Data for Modeling
- Nested data is ideal for fitting models across groups.
- Each subset in a list-column can hold an individual model or analysis result.

---

## Practical Example: Nesting `mtcars` for Modeling
- Group `mtcars` by `cyl` (number of cylinders) and nest data within each group.
```r
# Nesting mtcars data by cylinder
mtcars_nested <- mtcars %>% group_by(cyl) %>% nest()
```

---

## Building Models on Nested Data
- Use `purrr::map()` to fit models within each nested group.
- Store each model in a new list-column.

```r
# Fit models to each subset
mtcars_nested <- mtcars_nested %>% 
  mutate(model = map(data, ~ lm(mpg ~ wt, data = .x)))
```

---

## Extracting Predictions from Nested Models
- Generate predictions for each model using `map()` to apply `predict()`.
- Efficient way to produce predictions for each group in a single step.

```r
# Generate predictions
mtcars_nested <- mtcars_nested %>%
  mutate(predictions = map(model, predict))
```

---

# Summarizing Model Results with `broom`

## Using `broom` to Tidy Model Outputs
- `broom` provides functions like `tidy()`, `augment()`, and `glance()` to convert model outputs to data frames.
- This allows for consistent analysis and visualization of multiple models' outputs.

---

## Practical Example: Tidying with `broom::tidy()`
```r
# Tidying model results
library(broom)
mtcars_nested <- mtcars_nested %>%
  mutate(tidy_results = map(model, tidy))

# Unnesting to view all results in a flat format
mtcars_nested %>% unnest(tidy_results)
```

---

## Advanced Tidying: `augment()` and `glance()`
- **`augment()`**: Adds model predictions and residuals to the original data.
- **`glance()`**: Summarizes model fit statistics.

```r
# Adding model summaries
mtcars_nested <- mtcars_nested %>%
  mutate(augmented = map(model, augment),
         glance_results = map(model, glance))
```

---

# Combining and Visualizing Model Summaries

## Workflow: Nest, Map, and Unnest
- Combine nested data manipulation and `broom` outputs for a complete summary.
- Use `unnest()` to organize results into a single, interpretable data frame.

```r
# Complete workflow with tidying and unnesting
mtcars_nested %>%
  unnest(c(tidy_results, augmented, glance_results))
```

---

## Practical Application: Model Comparison
- Easily compare models across groups with tidied outputs.
- Sort or filter by fit statistics, visualize parameter estimates, or compare residuals.

```r
# Example: Sorting by R-squared from glance results
mtcars_nested %>%
  unnest(glance_results) %>%
  arrange(desc(r.squared))
```

---