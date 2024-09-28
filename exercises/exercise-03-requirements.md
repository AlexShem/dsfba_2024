# Series 3: Control Flow and Functions in R

The third exercise session, focusing on control flow and functions, is designed to help students practice the key concepts covered in Lecture 3, emphasizing practical skills directly applicable to data analysis in R.

## Exercise 1: Creating Loops (`for` and `while`)

### Objective

Practice creating loops to automate repetitive tasks

### Task

1. `for` Loop Exercise:
   - Write a `for` loop that iterates over a sequence of numbers from 1 to 10.
   - For each iteration, calculate the square of the current number and print the result.
2. `while` Loop Exercise:
   - Write a `while` loop that starts with a value of 1 and doubles it until it exceeds 1000.
   - Print each value of the loop to observe the progression.

### Expected Skills

Understanding loop syntax, controlling iterations, and managing conditions within loops.

## Exercise 2: Creating a Custom Function

### Objective

Develop skills in writing reusable functions for data analysis tasks.

### Task

- Create a custom function named `z_score(x, value)` that calculates the z-score of a value given the sample vector `x`.
- The z-score is calculated as `(value - mean(x)) / sd(x)`, where `x` is the sample vector and `value` is the value for which the z-score is calculated.
- Use the function on a sample from a normal distribution to test its functionality.

### Example Code

```r
z_score <- function(x, value = 0) {
    # Check if inputs are numeric
    if (!is.numeric(x)) {
        stop("Sample vector must be numeric.")
    }
    if (!is.numeric(value)) {
        stop("Value must be numeric.")
    }
    (value - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE)
}

# Test the function with a sample data vector
sample_data <- rnorm(100)
z_score(sample_data)

# Test the function with a value argument
sample_data_with_na <- c(rnorm(50), NA)
z_score(sample_data_with_na, value = 2)
```

### Expected Skills

Defining functions, using conditional checks, and testing functions on data.

## Exercise 3: Applying a Custom Function on the `mtcars` Dataset using `purrr`

### Objective

Apply custom functions to data frames using `purrr` to efficiently process multiple columns, ensuring the output remains a `tibble`.

### Task

1. Convert the `mtcars` dataset to a `tibble` using the `tibble` package to work with a tidy format that integrates well with the `tidyverse`.
1. Create a custom function named `scale_min_max()` that scales a numeric vector to a 0-1 range using the formula: `(x - min(x)) / (max(x) - min(x))`.
1. Use the `modify_if()` function from the `purrr` package to apply `scale_min_max()` to all numeric columns of the mtcars tibble, ensuring the output remains a `tibble`.

### Example Code

```r
# Load necessary packages
library(dplyr)
library(purrr)
library(tibble)

# Convert mtcars dataset to a tibble
mtcars_tibble <- as_tibble(mtcars)

# Custom function to scale values between 0 and 1
scale_min_max <- function(x) {
  (x - min(x, na.rm = TRUE)) / (max(x, na.rm = TRUE) - min(x, na.rm = TRUE))
}

# Apply the function to all numeric columns in the tibble and keep the output as a tibble
scaled_mtcars <- mtcars_tibble %>%
  modify_if(is.numeric, scale_min_max)

# Display the first few rows of the scaled tibble
print(scaled_mtcars)
```

### Expected Skills

- Converting Data Frames to Tibbles: Using `as_tibble()` to work seamlessly with `tidyverse` functions.
- Creating Custom Functions: Writing reusable functions for data transformation tasks.
- Using purrr Functions (`modify_if()`): Applying custom transformations to specific columns while maintaining the `tibble` structure.

## Instructions for Captains

1. Ensure that each exercise is clearly stated with a brief introduction to the objective.
1. Provide clear and concise examples for students to follow.
1. Include brief explanations of expected skills and learning outcomes for each task.
1. Keep the exercises concise to avoid overwhelming students, focusing on practical, directly applicable skills.
1. Ensure that the exercises are ready for student distribution with proper formatting and instructions on the expected output.

These exercises will allow students to practice essential programming paradigms, focusing on practical skills relevant to data science applications in R.
