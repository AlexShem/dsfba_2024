# Exercise Session: Data Structures in R

## Overview

This exercise session will help students practice basic data structures in R, including vectors, lists, data frames, and `tibble`s. The exercises emphasize `tibble`s, preparing students for future data analysis work with the `tidyverse`.

## Exercise Problems

### 1. Working with Vectors

**Objective**: Understanding and manipulating atomic vectors.

- **Problem 1.1**: Create different types of atomic vectors (logical, integer, double, character). Use `typeof()`, `length()`, and `attributes()` functions to inspect these vectors.
  
- **Problem 1.2**: Combine vectors using `c()` and explore coercion rules by mixing different types of data. Use `as.<type>()` functions to coerce vectors explicitly and observe the changes.

- **Problem 1.3**: Practice subsetting vectors using positive/negative indices, logical conditions, and named subsetting.

### 2. Lists and Their Use Cases

**Objective**: Learning how to work with lists, which can store heterogeneous types of data.

- **Problem 2.1**: Create a list containing different data types (numeric vector, character, logical). Use `str()` to inspect the structure.
  
- **Problem 2.2**: Subset lists using `[]` and `[[` operators and compare the outputs.

### 3. Introduction to Data Frames

**Objective**: Understanding data frames as a fundamental data structure in R.

- **Problem 3.1**: Create a simple data frame using `data.frame()`. Add and modify columns using `$` and subsetting techniques.
  
- **Problem 3.2**: Subset data frames by selecting specific rows and columns using logical conditions and column names.

### 4. Introduction to Tibbles

**Objective**: Introducing `tibble`s, the modern alternative to data frames, with a focus on their unique features.

- **Problem 4.1**: Create a `tibble` using the `tibble()` function.

- **Problem 4.2**: Experiment with creating a `tibble` with non-syntactic names. Use backticks (`) to access columns with unconventional names.

- **Problem 4.3**: Compare outputs when subsetting a single column with `[ ]` and `[[ ]]`.

### 5. Advanced: Practical Data Analysis Task

**Objective**: Applying knowledge of data structures in a small analysis task.

> Note: The functionality of `tidyverse` packages like `dplyr` and `tidyr` are not covered in this lecture. However, advanced students can try using them for data manipulation tasks.

- **Problem 5.1**: Load a dataset (e.g., `mtcars` or `iris`) and convert it to a `tibble`. Perform basic data manipulation such as filtering rows, selecting columns, and mutating new columns.

- **Problem 5.2**: Use functions like `summarize()` and `group_by()` from `dplyr` to calculate summary statistics, demonstrating the seamless use of `tibble`s in data analysis workflows.

## Expected Structure of Exercises

- Each problem should be followed by list of steps and hints to guide students.
- Encourage using `?` and `help()` for exploring function documentation.
- After the exercise session, provide for students the same document complemented with solutions to self-assess their understanding.

## Tips for Instructors

- @Ilia: Make an approximate 5-10-mintue introduction to the problems at the beginning of the session.
- Highlight the importance of `tibble`s in modern data analysis and why they are preferred over traditional data frames in the `tidyverse`.
- Use this session to build familiarity with R's syntax and help students transition comfortably to using `tibble`s for future data analysis tasks.
