import constants
import distributions
import streamlit as st

class Job:
    job_number = 0  
    def __init__(self, education_level):
        self.id = Job.job_number
        Job.job_number += 1
        self.education_level = education_level
        # self.salary = constants.median_earning_by_education[education_level]
        self.open = True
        self.worker = None
        # possible_high_earner = constants.education.AdvancedDegree or constants.education.Bachelor

        median_salary = constants.st.session_state.MEDIAN_EARNING_BY_EDUCATION[education_level]
        self.salary = distributions.generate_salary_from_normal_with_outliers(
            median_salary)
        

    def hire(self, worker):
        self.open = False
        self.worker = worker
        
    def fire(self):
        self.open = True
        self.worker.remove_job()
        self.worker = None
        
    def open_job(self):
        self.open = True
        self.worker = None

    def display(self):
        pass
    
    def simulate(self):
        #  do something with some probability to simulate the passage of time
        pass
