import constants
import worker
import numpy as np
from math import floor
import job


class LaborMarket:
    education_levels = list(constants.EDUCATION_DISTRIBUTION.keys())
    education_probabilities = list(constants.EDUCATION_DISTRIBUTION.values())

    def __init__(self, working_population, use_net_unemployment_rate=False, standardize_jobs=False):

        self.working_population = working_population

        self.generated_educations = np.random.choice(
            self.education_levels, size=working_population, p=self.education_probabilities)

        # generates workers from generated educations
        self.workers = []

        self.workers_by_education = {
            edu: [] for edu in self.education_levels}
        for edu in self.generated_educations:
            generated_worker = worker.worker(edu)
            self.workers_by_education[edu].append(generated_worker)
            self.workers.append(generated_worker)

            # generate jobs based on the number of each worker
        self.number_of_open_jobs_per_education = {}
        if standardize_jobs:
            # number of jobs for each education level is constant
            for edu in self.education_levels:
                employment_rate = 1 - \
                    constants.UNEMPLOYMENT_RATE_BY_EDUCATION[edu]

                self.number_of_open_jobs_per_education[edu] = floor(working_population *
                                                                    self.education_probabilities[edu] * employment_rate)
        else:
            # number of jobs for each education level is determined by the generated distribution
            for edu in self.education_levels:
                unadjusted_num_jobs_per_edu_level = np.sum(
                    self.generated_educations == edu)

                if use_net_unemployment_rate:
                    self.number_of_open_jobs_per_education[edu] = floor(
                        unadjusted_num_jobs_per_edu_level * (1 - constants.NET_UNEMPLOYMENT_RATE))
                else:
                    self.number_of_open_jobs_per_education[edu] = floor(
                        unadjusted_num_jobs_per_edu_level * (1 - constants.UNEMPLOYMENT_RATE_BY_EDUCATION[edu]))

        # generate jobs
        self.open_jobs_by_education = {
            edu: [] for edu in self.education_levels}

        for edu in self.education_levels:
            for _ in range(self.number_of_open_jobs_per_education[edu]):
                self.open_jobs_by_education[edu].append(
                    job.Job(edu))

    def match(self):
        # match workers to jobs
        self.matched_jobs = {edu: [] for edu in self.education_levels}
        self.matched_workers = {edu: [] for edu in self.education_levels}

        earning_threshold = 0.2

        for edu in self.education_levels:
            n = max(3, self.number_of_open_jobs_per_education[edu])
            for worker in self.workers_by_education[edu]:

                if worker.employed:
                    continue

                # take a random sample of jobs to simulate job search
                available_jobs = np.random.choice(
                    self.open_jobs_by_education[edu], size=min(
                        n, len(self.open_jobs_by_education[edu])), replace=False)

                min_wage = worker.expected_earning * (1 - earning_threshold)
                max_wage = worker.expected_earning * (1 + earning_threshold)
                filtered_jobs = [
                    job for job in available_jobs if job.salary >= min_wage and job.salary <= max_wage]

                if not filtered_jobs:
                    continue

                # choose the highest paying job that the worker is qualifed for
                best_job = max(filtered_jobs, key=lambda job: job.salary)

                worker.hire(best_job)
                best_job.hire()

                # remove the job from the list of open jobs
                self.open_jobs_by_education[edu].remove(best_job)

    def get_workers(self):
        return self.workers
