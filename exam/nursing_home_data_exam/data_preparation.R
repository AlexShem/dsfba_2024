library(tidyverse)
library(here)

load(here("exam/nursing_home_data/data_OPAS.RData"))

set.seed(1234)
n_sample <- 10000

## Sample the Individuals from the `data_ind`

demographics <- data_ind %>%
  mutate(id_row = row_number(), .before = indiv_id) %>%
  slice_sample(n = min(n_sample, nrow(data_ind))) %>%
  arrange(id_row)

health_screenings <- data_img %>%
  semi_join(demographics, by = join_by(indiv_id))

## Select the desired columns

demographics <- demographics %>%
  select(
    RowId = id_row,
    PatientID = indiv_id,
    DateOfBirth = date_birth,
    Gender = gender,
    DateOfAdmission = date_entry,
    DateOfDeath = date_exit
  )

health_screenings <- health_screenings %>%
  select(
    PatientID = indiv_id,
    ScreeningDate = date_img,
    DependenceLevel = DP,
    PhysicalMobility = PM,
    PrimaryDiagnosis = D1,
    SecondaryDiagnosis = D2,
    CareMinutesPerWeek = min_total
  )

## Modify the values

# Anonymise the patient ID
demographics <- demographics %>%
  mutate(ID_anon = fct_anon(PatientID, prefix = "P"), .after = PatientID)

health_screenings <- health_screenings %>%
  left_join(demographics %>% select(PatientID, ID_anon), by = join_by(PatientID))

# Restore the `PatientID` columns
demographics <- demographics %>%
  mutate(PatientID = ID_anon, .keep = "unused")

health_screenings <- health_screenings %>%
  mutate(PatientID = ID_anon, .keep = "unused")

# Modify the `Gender` column
demographics <- demographics %>%
  mutate(Gender = fct_recode(Gender, Female = "F", Male = "M"))

# Add random time to the `DateOfDeath` column using `lubridate`
demographics <- demographics %>%
  mutate(
    DateOfDeath = map_vec(
      DateOfDeath,
      \(date) as_datetime(
        date +
          hours(sample.int(24, 1)) +
          minutes(sample.int(60, 1)) +
          seconds(sample.int(60, 1))
      )
    )
  )

# Add random time to the `ScreeningDate` column using `lubridate`
health_screenings <- health_screenings %>%
  mutate(
    ScreeningDate = map_vec(
      ScreeningDate,
      \(date) as_datetime(
        date +
          hours(sample.int(24, 1)) +
          minutes(sample.int(60, 1)) +
          seconds(sample.int(60, 1))
      )
    )
  )

## Save the data
write_csv(demographics, here("exam/nursing_home_data_exam/demographics.csv"))

write_csv(health_screenings, here("exam/nursing_home_data_exam/health_screenings.csv"))
