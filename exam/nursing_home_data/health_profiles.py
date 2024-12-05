import numpy as np
from enum import Enum, auto
import scipy.stats as stats

# Global RNG that will be set for the main script
seed = 423183873923
rng = np.random.default_rng(seed)

# care_minutes_dist parameters
care_minutes_coefficients = {
    "intercept": {
        # "beta": -3.4955,
        # "theta": 5.6313,
        "beta": -3.4,
        "theta": 5.4,
    },
    "gender": {
        "Female": {
            "beta": 0,
            "theta": 0
        },
        "Male": {
            "beta": 0.0684,
            "theta": -0.0793
        }
    },
    "dependence_level": {
        "1-6": {
            "beta": 0,
            "theta": 0
        },
        "7": {
            "beta": 0.4308,
            "theta": -1.0442
        },
        "8": {
            "beta": 0.6946,
            "theta": -0.7241
        },
        "9": {
            "beta": 0.9084,
            "theta": -0.7383
        }
    },
    "mobility_level": {
        "1-5": {
            "beta": 0,
            "theta": 0
        },
        "6": {
            "beta": 0.1756,
            "theta": -0.1266
        },
        "7": {
            "beta": 0.3212,
            "theta": -0.0973
        },
        "8": {
            "beta": 0.3838,
            "theta": -0.0077
        },
        "9": {
            "beta": 0.5207,
            "theta": 0.4890
        }
    },
    "primary_diagnosis": {
        "Mental": {
            "beta": 0,
            "theta": 0
        },
        "Nervous": {
            "beta": 0.0332,
            "theta": -0.0244
        },
        "Osteoarticular": {
            "beta": 0.0229,
            "theta": -0.1177
        },
        "Tumour": {
            "beta": 0.0328,
            "theta": -0.0171
        },
        "Other": {
            "beta": 0.0358,
            "theta": -0.0864
        }
    }
}

# survival_time_dist parameters
suvival_time_coefficients = {
    # "intercept": 4.9862,
    "intercept": 6,
    "ln_sigma": -0.2702,
    "gender": {
        "Female": 0,
        "Male": -0.3884
    },
    "dependence_level": {
        "1-6": 0,
        "7": -0.0750,
        "8": -0.2532,
        "9": -0.5687
    },
    "mobility_level": {
        "1-5": 0,
        "6": -0.1407,
        "7": -0.2299,
        "8": -0.2930,
        "9": -0.2842
    },
    "primary_diagnosis": {
        "Mental": 0,
        "Nervous": -0.0821,
        "Osteoarticular": 0.0276,
        "Tumour": -0.8512,
        "Other": -0.1266
    }
}

class HealthProfileType(Enum):
    RELATIVELY_INDEPENDENT = auto()
    VERY_DEPENDENT = auto()
    VERY_DEPENDENT_NERVOUS = auto()
    MODERATELY_DEPENDENT_TUMOUR = auto()

def calculate_survival_parameters(gender, dependence_level, mobility_level, primary_diagnosis):
    """Calculate Weibull distribution parameters based on coefficients."""
    mu = suvival_time_coefficients["intercept"]
    mu += suvival_time_coefficients["gender"][gender]
    
    dep_key = str(dependence_level) if dependence_level > 6 else "1-6"
    mu += suvival_time_coefficients["dependence_level"][dep_key]
    
    mob_key = str(mobility_level) if mobility_level > 5 else "1-5"
    mu += suvival_time_coefficients["mobility_level"][mob_key]
    
    mu += suvival_time_coefficients["primary_diagnosis"][primary_diagnosis]
    
    sigma = np.exp(suvival_time_coefficients["ln_sigma"])
    return mu, sigma

def calculate_care_parameters(gender, dependence_level, mobility_level, primary_diagnosis):
    """Calculate Beta distribution parameters based on coefficients."""
    beta = care_minutes_coefficients["intercept"]["beta"]
    theta = care_minutes_coefficients["intercept"]["theta"]
    
    beta += care_minutes_coefficients["gender"][gender]["beta"]
    theta += care_minutes_coefficients["gender"][gender]["theta"]
    
    dep_key = str(dependence_level) if dependence_level > 6 else "1-6"
    beta += care_minutes_coefficients["dependence_level"][dep_key]["beta"]
    theta += care_minutes_coefficients["dependence_level"][dep_key]["theta"]
    
    mob_key = str(mobility_level) if mobility_level > 5 else "1-5"
    beta += care_minutes_coefficients["mobility_level"][mob_key]["beta"]
    theta += care_minutes_coefficients["mobility_level"][mob_key]["theta"]
    
    beta += care_minutes_coefficients["primary_diagnosis"][primary_diagnosis]["beta"]
    theta += care_minutes_coefficients["primary_diagnosis"][primary_diagnosis]["theta"]
    
    return beta, theta

class HealthProfile:
    def __init__(self, profile_type):
        self.profile_type = profile_type
        self.set_parameters()
        # Initialize patient parameters
        self.gender = None
        self.dependence_level = None
        self.mobility_level = None
        self.primary_diagnosis = None
        self.generate_patient_parameters()

    def set_parameters(self):
        dependence_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        if self.profile_type == HealthProfileType.RELATIVELY_INDEPENDENT:
            self.gender_probs = {'Female': 0.775, 'Male': 0.225}
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
            self.gender_probs = {'Female': 0.775, 'Male': 0.225}
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
            self.gender_probs = {'Female': 0.695, 'Male': 0.305}
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
            self.gender_probs = {'Female': 0.523, 'Male': 0.477}
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

    def generate_patient_parameters(self):
        """Generate basic health parameters for the patient."""
        self.gender = rng.choice(
            list(self.gender_probs.keys()),
            p=list(self.gender_probs.values())
        )
        self.dependence_level = self.dependence_level_dist()
        self.mobility_level = self.mobility_level_dist()
        self.primary_diagnosis = self.primary_diagnosis_dist(['Mental', 'Nervous', 'Osteoarticular', 'Tumour', 'Other'])

    def get_dependence_level(self):
        return self.dependence_level_dist()

    def get_mobility_level(self):
        return self.mobility_level_dist()

    def get_care_minutes(self):
        """Generate care minutes using Beta distribution with calculated parameters."""
        beta, theta = calculate_care_parameters(
            self.gender, 
            self.dependence_level, 
            self.mobility_level, 
            self.primary_diagnosis
        )
        # Transform beta parameters to get values in realistic range
        mu = 1/(1 + np.exp(-beta))
        phi = np.exp(theta)
        alpha = mu * phi
        beta = (1 - mu) * phi
        # Scale to get realistic minutes (e.g., between 0 and 2000 minutes per week)
        return 10080 * stats.beta.rvs(alpha, beta, random_state=rng)

    def get_primary_diagnosis(self, diagnoses):
        return self.primary_diagnosis_dist(diagnoses)

    def get_survival_time(self):
        """Generate survival time using Weibull distribution with calculated parameters."""
        mu, sigma = calculate_survival_parameters(
            self.gender,
            self.dependence_level,
            self.mobility_level,
            self.primary_diagnosis
        )
        # Transform parameters for Weibull distribution
        scale = np.exp(mu)
        shape = 1/sigma
        return stats.weibull_min.rvs(shape, loc=0, scale=2*scale, random_state=rng)
