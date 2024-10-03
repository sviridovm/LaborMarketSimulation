import constants
import distributions


class Job:
    def __init__(self, education_level):
        self.education_level = education_level
        # self.salary = constants.median_earning_by_education[education_level]
        self.open = True

        # possible_high_earner = constants.education.AdvancedDegree or constants.education.Bachelor

        median_salary = constants.MEDIAN_EARNING_BY_EDUCATION[education_level]
        self.salary = distributions.generate_salary_from_normal_with_outliers(
            median_salary)

    def hire(self):
        self.open = False

    def display(self):
        pass
