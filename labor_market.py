import constants
import worker
import numpy as np
from math import floor
import job
import event
import streamlit as st

class LaborMarket:
    
    earning_threshold = 0.2


    def __init__(self, working_population, use_net_unemployment_rate=False, standardize_jobs=False):

        


        # must be evaluated at runtime to get the most complete values
        self.education_levels = list(constants.st.session_state.EDUCATION_DISTRIBUTION.keys())
        self.education_probabilities = list(constants.st.session_state.EDUCATION_DISTRIBUTION.values())

        self.working_population = working_population
        self.employed_worker_count = 0
        self.open_job_count = 0
        self.time = 0
        
        self.generated_educations = np.random.choice(
            self.education_levels, size=working_population, p=self.education_probabilities)

        self.workers = []
        self.jobs = []
        

        
        # generates workers from generated educations
        

        self.unemployed_workers_by_education = {
            edu: [] for edu in self.education_levels}
        for edu in self.generated_educations:
            generated_worker = worker.Worker(edu)
            self.unemployed_workers_by_education[edu].append(generated_worker)
            self.workers.append(generated_worker)

            # generate jobs based on the number of each worker
        self.number_of_open_jobs_per_education = {}
        if standardize_jobs:
            # number of jobs for each education level is constant
            for edu in self.education_levels:
                employment_rate = 1 - \
                    constants.st.session_state.UNEMPLOYMENT_RATE_BY_EDUCATION[edu]

                self.number_of_open_jobs_per_education[edu] = floor(working_population *
                                                                    self.education_probabilities[edu] * employment_rate)
        else:
            # number of jobs for each education level is determined by the generated distribution
            for edu in self.education_levels:
                unadjusted_num_jobs_per_edu_level = np.sum(
                    self.generated_educations == edu)

                if use_net_unemployment_rate:
                    self.number_of_open_jobs_per_education[edu] = floor(
                        unadjusted_num_jobs_per_edu_level * (1 - constants.st.session_state.NET_UNEMPLOYMENT_RATE))
                else:
                    self.number_of_open_jobs_per_education[edu] = floor(
                        unadjusted_num_jobs_per_edu_level * (1 - constants.st.session_state.UNEMPLOYMENT_RATE_BY_EDUCATION[edu]))

        # generate jobs
        self.open_jobs_by_education = {
            edu: [] for edu in self.education_levels}

        for edu in self.education_levels:
            for _ in range(self.number_of_open_jobs_per_education[edu]):
                generated_job = job.Job(edu)
                self.open_jobs_by_education[edu].append(
                    generated_job)
                self.jobs.append(generated_job)
                
                
        self.match()
        self.reconstruct()
        self.metrics = Metrics(self)
        

    def match(self, num_iter=5):
        # match workers to jobs

        if num_iter == 0:
            return


        # must have job with same edu level
        for edu in self.education_levels:
            n = max(10, self.number_of_open_jobs_per_education[edu])
            
            
            for worker in self.unemployed_workers_by_education[edu]:

                if worker.employed:
                    continue

                # take a random sample of jobs to simulate job search
                available_jobs = np.random.choice(
                    self.open_jobs_by_education[edu], size=min(
                        10, len(self.open_jobs_by_education[edu])), replace=False)

                min_wage = worker.expected_earning * (1 - self.earning_threshold)
                max_wage = worker.expected_earning * (1 + self.earning_threshold)
                filtered_jobs = [
                    job for job in available_jobs if job.salary >= min_wage and job.salary <= max_wage]

                if not filtered_jobs:
                    continue

                # choose the highest paying job that the worker is qualifed for
                best_job = max(filtered_jobs, key=lambda job: job.salary)
                

                self._match(worker, best_job)

                # remove the job from the list of open jobs
                self.open_jobs_by_education[edu].remove(best_job)
                self.unemployed_workers_by_education[edu].remove(worker)
                self.number_of_open_jobs_per_education[edu] -= 1

        self.match(num_iter - 1)

    def get_workers(self):
        return self.workers
    
    
    
    # Create jobs proportional to unfilled worker demand
    def worker_feedback_job_creation(self, inefficiency=0.1):
        for edu in self.education_levels:
            num_unemployed = len(self.unemployed_workers_by_education[edu])
            total_workers = len([worker for worker in self.workers if worker.employed])
            
            unemployment_rate = num_unemployed / total_workers
             
            
            # economy adjusts to create more jobs
            if unemployment_rate > st.session_state.UNEMPLOYMENT_RATE_BY_EDUCATION[edu]:
                num_jobs = floor(num_unemployed * inefficiency)
                for _ in range(num_jobs):
                    generated_job = job.Job(edu)
                    self.open_jobs_by_education[edu].append(
                        generated_job)
                    self.jobs.append(generated_job)
            else:
                # economy adjusts to remove jobs
                num_jobs = floor(num_unemployed * inefficiency)
                self.jobs.sort(key=lambda job: not job.open)
                
                # remove the last n jobs
                for _ in range(num_jobs):
                    job = self.jobs.pop()
                    job.open = False
                    job.worker.remove_job()
                    job.worker = None
                    self.open_jobs_by_education[job.education_level].remove(job)
                    self.number_of_open_jobs_per_education[job.education_level] -= 1
    
    
    def simulate(self):
        self.time += 1

        # apply macro level events
        event.inflation.apply(self, self.time)

        for worker in self.workers:
            worker.simulate()
        
        for job in self.jobs:
            job.simulate()
        
        
        self.reconstruct()
            
        self.match()
        self.metrics.update()
        
        
        
        
    def bidirectional_match(self):
        # Priority queues for matching
        job_queue = {edu: sorted(self.open_jobs_by_education[edu], key=lambda job: -job.salary)
                    for edu in self.education_levels}
        worker_queue = {edu: sorted(self.unemployed_workers_by_education[edu], key=lambda w: w.expected_earning)
                        for edu in self.education_levels}

        # Match workers and jobs
        for edu in self.education_levels:
            while job_queue[edu] and worker_queue[edu]:
                worker = worker_queue[edu].pop(0)  # Get the worker with the lowest expectations
                job = job_queue[edu].pop(0)       # Get the highest-paying job

                if worker.expected_earning * (1 - self.earning_threshold) <= job.salary <= worker.expected_earning * (1 + self.earning_threshold):
                    # Match worker and job
                    # worker.hire(job)
                    # job.hire()
                    # self.matches.append(Match(job, worker))
                    pass
                else:
                    # Put unmatched job back for another round
                    job_queue[edu].append(job)


    def _match(self, worker, job):
        # Match worker and job
        worker.hire(job)
        job.hire(worker)

        
    def reconstruct(self):
        # Reconstruct the unemployed workers and open jobs
        self.unemployed_workers_by_education = {
            edu: [] for edu in self.education_levels}
        for worker in self.workers:
            if not worker.employed:
                self.unemployed_workers_by_education[worker.education_level].append(
                    worker)



        self.open_jobs_by_education = {
            edu: [] for edu in self.education_levels}
        for job in self.jobs:
            if job.open:
                self.open_jobs_by_education[job.education_level].append(job)
        
        self.number_of_open_jobs_per_education = {
            edu: len(jobs) for edu, jobs in self.open_jobs_by_education.items()}
        
        self.employed_worker_count = len([worker for worker in self.workers if worker.employed])
        self.open_job_count = len([job for job in self.jobs if job.open])


# class Match:
#     def __init__(self, job, worker):
#         self.job = job
#         self.worker = worker
        
#         self.job.hire(worker)
#         self.worker.hire(job)
    
#     def simulate(self):
#         quit_job = self.worker.simulate()
#         self.job.simulate()
        
        
        
        
class Metrics:
    
    def __init__(self, labor_market):
        self.labor_market = labor_market
        
        # self.avg_salaries = [self.calculate_average_salaries()]
        # self.unemployment_rates = [self.calculate_unemployment_rate()]
        # self.total_savings = [np.sum([worker.savings for worker in self.labor_market.workers])]
        # self.total_COL = [np.sum([worker.adjusted_COL for worker in self.labor_market.workers])]
        # self.avg_COL = [np.mean([worker.adjusted_COL for worker in self.labor_market.workers])]
        # self.total_savings = [np.sum([worker.savings for worker in self.labor_market.workers])]
        
        self.avg_salaries = []
        self.unemployment_rate = []
        self.total_savings = []
        self.total_COL = []
        self.avg_COL = []
        self.total_savings = []
        self.avg_savings = []
        self.num_employed = []
        
        self.update()
        
    
    def update(self):
        self.avg_salaries.append(self.calculate_average_salaries())
        self.unemployment_rate.append(self.calculate_unemployment_rate())
        self.total_savings.append(np.sum([worker.savings for worker in self.labor_market.get_workers()]))
        self.total_COL.append(np.sum([worker.adjusted_COL * 365 for worker in self.labor_market.get_workers()]))
        self.avg_COL.append(np.mean([worker.adjusted_COL * 365 for worker in self.labor_market.get_workers()]))
        self.total_savings.append(np.sum([worker.savings for worker in self.labor_market.get_workers()]))
        self.avg_savings.append(np.mean([worker.savings for worker in self.labor_market.get_workers()]))
        
        
    
    def calculate_average_salaries(self):
        total = np.sum([worker.job.salary for worker in self.labor_market.get_workers() if worker.employed])
        employed = len([worker for worker in self.labor_market.get_workers() if worker.employed])
        return total / employed
    
    def calculate_unemployment_rate(self):
        return 1 - (self.labor_market.employed_worker_count / self.labor_market.working_population)


    