import numpy as np
from enum import Enum, auto

# Global RNG that will be set for the main script
seed = 423183873923
rng = np.random.default_rng(seed)

class HealthProfileType(Enum):
    RELATIVELY_INDEPENDENT = auto()
    VERY_DEPENDENT = auto()
    VERY_DEPENDENT_NERVOUS = auto()
    MODERATELY_DEPENDENT_TUMOUR = auto()

class HealthProfile:
    def __init__(self, profile_type):
        self.profile_type = profile_type
        self.set_parameters()

    def set_parameters(self):
        dependence_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        if self.profile_type == HealthProfileType.RELATIVELY_INDEPENDENT:
            dependence_prevalence = [1, 2, 3, 4, 5, 10, 8, 4, 4]
            mobility_prevalence = [1, 2, 3, 4, 9, 10, 6, 5, 4]
            
            self.dependence_level_dist = lambda: rng.choice(
                dependence_levels,
                p=[p/sum(dependence_prevalence) for p in dependence_prevalence]
            )
            self.mobility_level_dist = lambda: rng.choice(
                dependence_levels,
                p=[p/sum(mobility_prevalence) for p in mobility_prevalence]
            )
            self.care_minutes_dist = lambda: rng.normal(150, 30)
            self.primary_diagnosis_dist = lambda diagnoses: rng.choice(diagnoses)
            self.survival_time_dist = lambda: rng.exponential(scale=6*365)  # 6 years average
        elif self.profile_type == HealthProfileType.VERY_DEPENDENT:
            dependence_prevalence = [1, 1, 1, 2, 5, 5, 9, 10, 7]
            mobility_prevalence = [1, 1, 1, 1, 2, 6, 9, 10, 9]
            
            self.dependence_level_dist = lambda: rng.choice(
                dependence_levels,
                p=[p/sum(dependence_prevalence) for p in dependence_prevalence]
            )
            self.mobility_level_dist = lambda: rng.choice(
                dependence_levels,
                p=[p/sum(mobility_prevalence) for p in mobility_prevalence]
            )
            self.care_minutes_dist = lambda: rng.normal(800, 50)
            self.primary_diagnosis_dist = lambda diagnoses: rng.choice(diagnoses)
            self.survival_time_dist = lambda: rng.exponential(scale=4*365)  # 4 years average
        elif self.profile_type == HealthProfileType.VERY_DEPENDENT_NERVOUS:
            dependence_prevalence = [1, 1, 1, 2, 5, 5, 9, 10, 7]
            mobility_prevalence = [1, 1, 1, 3, 4, 6, 10, 8, 8]
            
            self.dependence_level_dist = lambda: rng.choice(
                dependence_levels,
                p=[p/sum(dependence_prevalence) for p in dependence_prevalence]
            )
            self.mobility_level_dist = lambda: rng.choice(
                dependence_levels,
                p=[p/sum(mobility_prevalence) for p in mobility_prevalence]
            )
            self.care_minutes_dist = lambda: rng.normal(900, 50)
            self.primary_diagnosis_dist = lambda diagnoses: 'Nervous'
            self.survival_time_dist = lambda: rng.exponential(scale=3.5*365)  # 3.5 year average
        elif self.profile_type == HealthProfileType.MODERATELY_DEPENDENT_TUMOUR:
            dependence_prevalence = [1, 1, 1, 2, 4, 5, 10, 8, 7]
            mobility_prevalence = [1, 1, 1, 3, 4, 6, 10, 8, 8]
            
            self.dependence_level_dist = lambda: rng.choice(
                dependence_levels,
                p=[p/sum(dependence_prevalence) for p in dependence_prevalence]
            )
            self.mobility_level_dist = lambda: rng.choice(
                dependence_levels,
                p=[p/sum(mobility_prevalence) for p in mobility_prevalence]
            )
            self.care_minutes_dist = lambda: rng.normal(500, 50)
            self.primary_diagnosis_dist = lambda diagnoses: 'Tumour'
            self.survival_time_dist = lambda: rng.exponential(scale=0.8*365)  # 0.8 years average

    def get_dependence_level(self):
        return self.dependence_level_dist()

    def get_mobility_level(self):
        return self.mobility_level_dist()

    def get_care_minutes(self):
        return max(0, self.care_minutes_dist())  # Ensure non-negative care minutes

    def get_primary_diagnosis(self, diagnoses):
        return self.primary_diagnosis_dist(diagnoses)

    def get_survival_time(self):
        return max(1, self.survival_time_dist())  # At least 1 day
