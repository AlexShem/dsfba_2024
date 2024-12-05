import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Import the health profiles module
from health_profiles import HealthProfileType, HealthProfile, rng

# ---------------------------
# Parameters
# ---------------------------

# Number of unique patients
NUM_PATIENTS = 5000

# Number of health observations distribution parameters
MIN_SCREENINGS_PER_PATIENT = 1
MAX_SCREENINGS_PER_PATIENT = 10
HEALTH_OBS_LAMBDA = 0.5  # Lambda for skewed distribution

# Date ranges for generating random dates
START_DATE_OF_BIRTH = datetime(1920, 1, 1)
END_DATE_OF_BIRTH = datetime(1970, 12, 31)
START_DATE_OF_ADMISSION = datetime(2000, 1, 1)
END_DATE_OF_ADMISSION = datetime(2023, 12, 31)
STUDY_END_DATE = datetime(2024, 12, 31)

# Gender probabilities
GENDER_PROBABILITIES = {'Male': 0.4, 'Female': 0.6}

# Primary and secondary diagnoses
PRIMARY_DIAGNOSES = [
    'Mental',
    'Nervous',
    'Respiratory',
    'Heart',
    'Osteoarticular',
    'Tumour'
]

# Probability of having a secondary diagnosis
SECONDARY_DIAGNOSIS_PROBABILITY = 0.9

# Project folder and filenames
PROJECT_FOLDER = 'exam/nursing_home_data'
DEMOGRAPHICS_FILENAME = 'demographics.csv'
HEALTH_SCREENINGS_FILENAME = 'health_screenings.csv'

# Proportion of patients in each health profile
HEALTH_PROFILE_PROBABILITIES = {
    HealthProfileType.RELATIVELY_INDEPENDENT: 0.4,
    HealthProfileType.VERY_DEPENDENT: 0.32,
    HealthProfileType.VERY_DEPENDENT_NERVOUS: 0.2,
    HealthProfileType.MODERATELY_DEPENDENT_TUMOUR: 0.08
}

# ---------------------------
# Helper Functions
# ---------------------------

def random_date(start, end):
    """
    Generate a random datetime between `start` and `end`.
    """
    delta = end - start
    int_delta = delta.days
    if int_delta <= 0:
        return start
    random_day = rng.integers(int_delta)
    return start + timedelta(days=int(random_day))

def generate_demographics(num_patients, start_dob, end_dob, start_admission, end_admission, gender_probs, health_profile_probs):
    """Generate demographic data for patients."""
    ids = ['P{:05d}'.format(i) for i in range(1, num_patients + 1)]
    dates_of_birth = [random_date(start_dob, end_dob) for _ in range(num_patients)]
    
    health_profiles = rng.choice(
        list(health_profile_probs.keys()),
        size=num_patients,
        p=list(health_profile_probs.values())
    )

    dates_of_admission = []
    dates_of_death = []
    genders = []
    
    profiles = []
    for i in range(num_patients):
        # Create profile and generate parameters
        profile = HealthProfile(health_profiles[i])
        profiles.append(profile)
        
        # Store gender
        genders.append(profile.gender)
        
        # Generate admission and death dates
        dob = dates_of_birth[i]
        min_admission_date = max(dob + timedelta(days=18*365), start_admission)
        admission_date = random_date(min_admission_date, end_admission)
        dates_of_admission.append(admission_date)

        survival_days = profile.get_survival_time()
        death_date = admission_date + timedelta(days=survival_days)
        if death_date > STUDY_END_DATE:
            death_date = pd.NaT
        dates_of_death.append(death_date)
    
    data = {
        'PatientID': ids,
        'DateOfBirth': dates_of_birth,
        'Gender': genders,
        'DateOfAdmission': dates_of_admission,
        'DateOfDeath': dates_of_death,
        'HealthProfile': [profile.profile_type.name for profile in profiles]
    }
    
    df = pd.DataFrame(data)
    df['DateOfBirth'] = pd.to_datetime(df['DateOfBirth'])
    df['DateOfAdmission'] = pd.to_datetime(df['DateOfAdmission'])
    df['DateOfDeath'] = pd.to_datetime(df['DateOfDeath'])
    return df, profiles

def generate_health_screenings(demographics_df, diagnoses, secondary_diag_prob):
    """
    Generate health screening data for patients.
    """
    records = []

    for index, row in demographics_df.iterrows():
        # Get patient's health profile
        profile_type = HealthProfileType[row['HealthProfile']]
        profile = HealthProfile(profile_type)

        # Determine number of screenings (skewed distribution)
        num_screenings = min(MAX_SCREENINGS_PER_PATIENT, max(MIN_SCREENINGS_PER_PATIENT, rng.geometric(p=HEALTH_OBS_LAMBDA)))
        # Generate screening dates based on exponential distribution
        screening_dates = []
        current_date = row['DateOfAdmission']
        end_date = row['DateOfDeath'] if pd.notnull(row['DateOfDeath']) else STUDY_END_DATE

        while len(screening_dates) < num_screenings and current_date < end_date:
            interval_days = rng.exponential(scale=365)  # Average one year
            current_date += timedelta(days=interval_days)
            if current_date > end_date:
                current_date = end_date
            screening_dates.append(current_date)
        
        for screening_date in screening_dates:
            dependence = profile.get_dependence_level()
            mobility = profile.get_mobility_level()
            primary_diag = profile.get_primary_diagnosis(diagnoses)
            if rng.random() < secondary_diag_prob:
                secondary_diag_choices = [d for d in diagnoses if d != primary_diag]
                secondary_diag = rng.choice(secondary_diag_choices)
            else:
                secondary_diag = pd.NA
            care_minutes = profile.get_care_minutes()
            record = {
                'PatientID': row['PatientID'],
                'ScreeningDate': screening_date,
                'DependenceLevel': dependence,
                'PhysicalMobility': mobility,
                'PrimaryDiagnosis': primary_diag,
                'SecondaryDiagnosis': secondary_diag,
                'CareMinutesPerWeek': care_minutes
            }
            records.append(record)
    df = pd.DataFrame(records)
    df['ScreeningDate'] = pd.to_datetime(df['ScreeningDate'])
    return df

# ---------------------------
# Main Execution
# ---------------------------

def main():
    # Generate demographics data
    demographics_df, profiles = generate_demographics(
        NUM_PATIENTS,
        START_DATE_OF_BIRTH,
        END_DATE_OF_BIRTH,
        START_DATE_OF_ADMISSION,
        END_DATE_OF_ADMISSION,
        GENDER_PROBABILITIES,
        HEALTH_PROFILE_PROBABILITIES
    )

    # Generate health screenings data
    health_screenings_df = generate_health_screenings(
        demographics_df,
        PRIMARY_DIAGNOSES,
        SECONDARY_DIAGNOSIS_PROBABILITY
    )

    # Create project folder if it doesn't exist
    if not os.path.exists(PROJECT_FOLDER):
        os.makedirs(PROJECT_FOLDER)

    # Save the datasets to CSV files
    demographics_df.to_csv(os.path.join(PROJECT_FOLDER, DEMOGRAPHICS_FILENAME), index=False)
    health_screenings_df.to_csv(os.path.join(PROJECT_FOLDER, HEALTH_SCREENINGS_FILENAME), index=False)

    print(f"Data saved in '{PROJECT_FOLDER}' folder.")

if __name__ == "__main__":
    main()
