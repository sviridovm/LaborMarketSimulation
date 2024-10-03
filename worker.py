import constants
import distributions
import job


class worker:
    worker_number = 0

    def __init__(self, education_level: constants.education):
        self.education_level = education_level
        # self.expected_earning = constants.median_earning_by_education[education_level]
        self.employed = False
        self.job = None
        self.id = worker.worker_number
        worker.worker_number += 1

        median_earning = constants.MEDIAN_EARNING_BY_EDUCATION[education_level]
        # self.expected_earning = distributions.generate_salary_from_normal(
        # median_earning)

        self.expected_earning = distributions.generate_salary_from_normal_with_outliers(
            median_earning, lower_factor=0.8)

        self.salary_history = [self.expected_earning]

    def display(self):
        pass

    def hire(self, job: job.Job):
        if self.employed:
            raise Exception("Worker is already employed")

        self.employed = True
        self.job = job
        self.salary_history.append(job.salary)
