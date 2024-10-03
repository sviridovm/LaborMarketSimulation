import numpy as np


def create_normal_with_outliers(n, median, lower_factor=0.8, upper_factor=5, outlier_ratio=0.05, std_dev=0.2):
    # Step 1: Generate normal distribution for the majority
    salaries = np.random.normal(
        median, std_dev * median, int(n * (1 - outlier_ratio)))

    min_salary = lower_factor * median
    max_salary = upper_factor * median

    # Step 2: Add outliers using a log-normal or Pareto distribution for the extreme right skew
    outlier_count = int(np.ceil((n * outlier_ratio)))
    # Adjust the spread of outliers
    outliers = np.random.lognormal(np.log(median), 1.2, outlier_count)
    outliers = np.clip(outliers, min_salary, max_salary)
    # Step 3: Clip the normal distribution to respect the lower and upper bounds
    salaries = np.clip(salaries, min_salary, max_salary)

    # Combine normal and outliers
    salaries = np.concatenate((salaries, outliers))

    return salaries


def generate_salary_from_normal_with_outliers(median, skew_factor=1.15, lower_factor=0.85):
    # generates salary from a log normal distribution with a right skew
    # the skew factor controls how much larger the mean is than the median

    sigma = np.sqrt(np.log(skew_factor ** 2))
    salary = np.random.lognormal(np.log(median), sigma)
    return max(salary, median*lower_factor)


def generate_salary_from_normal(median, range=0.2):
    # generates a single salary from a normal distribution
    # return np.random.normal(median, median * std_dev)
    min_salary = median - median * range
    max_salary = median + median * range

    std_dev = (max_salary - min_salary) / 6
    # return np.random.uniform(min_salary, max_salary)
    return np.random.normal(median, std_dev)
