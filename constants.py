from enum import Enum


education = Enum(
    'education', ['Zero', 'Highschool', 'CollegeNoDegree', 'Associate', 'Bachelor', 'AdvancedDegree'])

EDUCATION_DISTRIBUTION = {
    education.Zero: 0.09,
    education.Highschool: 0.28,
    education.CollegeNoDegree: 0.15,
    education.Associate: 0.10,
    education.Bachelor: 0.24,
    education.AdvancedDegree: 0.14
}

# statisics from 2022 census


MEDIAN_EARNING_BY_EDUCATION = {
    education.Zero: 35500,
    education.Highschool:  41800,
    education.CollegeNoDegree: 45200,
    education.Associate: 49500,
    education.Bachelor: 66600,
    education.AdvancedDegree: 80200
}


# https://www.bls.gov/emp/chart-unemployment-earnings-education.htm
UNEMPLOYMENT_RATE_BY_EDUCATION = {
    education.Zero: 0.056,
    education.Highschool: 0.039,
    education.CollegeNoDegree: 0.033,
    education.Associate: 0.027,
    education.Bachelor: 0.022,
    education.AdvancedDegree: 0.016
}

NET_UNEMPLOYMENT_RATE = 0.03
