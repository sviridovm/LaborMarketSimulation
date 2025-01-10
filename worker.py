import constants
import distributions
import job
import numpy as np


class Worker:
    worker_number = 0
    # locations = list(constants.st.session_state.LOCATION_DISTRIBUTION.keys())
    # location_probabilities = list(constants.st.session_state.LOCATION_DISTRIBUTION.values())


    def __init__(self, education_level):
        self.education_level = education_level
        # self.expected_earning = constants.median_earning_by_education[education_level]
        self.employed = False
        self.job = None
        self.id = Worker.worker_number
        Worker.worker_number += 1
        
        self.location = np.random.choice(
            list(constants.st.session_state.LOCATION_DISTRIBUTION.keys()), 
            p=list(constants.st.session_state.LOCATION_DISTRIBUTION.values()))
        
        
        # print('*'*100)
        # print(constants.st.session_state.COL_LOCATION_FACTOR)
        # print(self.location)
        # print(self.location in constants.st.session_state.COL_LOCATION_FACTOR)
        
        self.adjusted_COL = constants.st.session_state.DAILY_COL * constants.st.session_state.COL_LOCATION_FACTOR[self.location]
        
        
        self.savings = 0

        median_earning = constants.st.session_state.MEDIAN_EARNING_BY_EDUCATION[education_level]
        # self.expected_earning = distributions.generate_salary_from_normal(
        # median_earning)

        self.expected_earning = distributions.generate_salary_from_normal_with_outliers(
            median_earning, lower_factor=0.8)

        self.salary_history = [0]
        
        self.events = [layoff, promotion]
        self.probabilities = [0.5, 0.5, ]

        self.worker_log = []
        
        
        self.adjusted_COL = constants.st.session_state.DAILY_COL
        

    def display(self):
        return (
                self.education_level.name,
                f'${int(self.salary_history[-1])}',
                self.location.name,
                int(self.adjusted_COL * 365),
                int(self.savings),
                self.employed,
                self.job.id if self.job else None
            )    

    def hire(self, job: job.Job):
        if self.employed:
            raise Exception("Worker is already employed")

        self.employed = True
        self.job = job
        self.salary_history.append(job.salary)
        
        self.worker_log.append(f"Worker {self.id} has been hired for job {job.id} with salary {job.salary}")

    def remove_job(self):
        self.employed = False
        if self.job:
            self.job.open_job()
            
        self.job = None
        self.salary_history.append(0)

    
    def simulate(self):
        
        if self.employed:
            self.savings += ( self.job.salary / 365) 

        self.savings -= self.adjusted_COL

        if np.random.rand() < 0.1:
            event = np.random.choice(self.events, p=self.probabilities)
            event.apply(self)
                

        # self.savings -= constants.MONTHLY_EXPENSES

    def update_salary(self, factor):
        if self.job is None:
            return
        
        self.job.salary = self.job.salary * factor
        self.salary_history.append(self.job.salary)
        self.expected_earning = self.job.salary

    def increase_education_level(self):
        
        self.education_level = constants.st.session_state.education(self.education_level.value + 1)
        self.expected_earning = distributions.generate_salary_from_normal_with_outliers(
            constants.st.session_state.MEDIAN_EARNING_BY_EDUCATION[self.education_level], lower_factor=0.8)
        # self.salary_history.append(self.expected_earning)
        
class workerEvent:
    def __init__(self, name, event):
        self.name = name
        self.event = event

    def apply(self, worker):
        # update the matches
        # labor_market.
        self.event(worker)
        worker.worker_log.append(f"Event {self.name} has been applied to worker {worker.id}")

    
    



layoff = workerEvent("Layoff", lambda worker: worker.remove_job())
burnout = workerEvent("Burnout", lambda worker: worker.remove_job())
promotion = workerEvent("Promotion", lambda worker: worker.update_salary(1.1))
# skill_up = workerEvent("Skill Up", lambda worker: worker.increase_education_level() )
