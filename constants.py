from enum import Enum
import streamlit as st


def init():

    education = Enum(
            'education', ['Zero', 'Highschool', 'CollegeNoDegree', 'Associate', 'Bachelor', 'AdvancedDegree'])


    if 'SIMULATION_READY' not in st.session_state:
        st.session_state.SIMULATION_READY = False

    if 'education' not in st.session_state:
        st.session_state.education = education

    if 'EDUCATION_DISTRIBUTION' not in st.session_state:
        st.session_state.EDUCATION_DISTRIBUTION = {
            st.session_state.education.Zero: 0.09,
            st.session_state.education.Highschool: 0.28,
            st.session_state.education.CollegeNoDegree: 0.15,
            st.session_state.education.Associate: 0.10,
            st.session_state.education.Bachelor: 0.24,
            st.session_state.education.AdvancedDegree: 0.14
        }
        

    # statisics from 2022 census

    if 'MEDIAN_EARNING_BY_EDUCATION' not in st.session_state:
        st.session_state.MEDIAN_EARNING_BY_EDUCATION = {
            st.session_state.education.Zero: 35500,
            st.session_state.education.Highschool:  41800,
            st.session_state.education.CollegeNoDegree: 45200,
            st.session_state.education.Associate: 49500,
            st.session_state.education.Bachelor: 66600,
            st.session_state.education.AdvancedDegree: 80200
        }


    # https://www.bls.gov/emp/chart-unemployment-earnings-education.htm

    if 'UNEMPLOYMENT_RATE_BY_EDUCATION' not in st.session_state:
        st.session_state.UNEMPLOYMENT_RATE_BY_EDUCATION = {
            st.session_state.education.Zero: 0.056,
            st.session_state.education.Highschool: 0.039,
            st.session_state.education.CollegeNoDegree: 0.033,
            st.session_state.education.Associate: 0.027,
            st.session_state.education.Bachelor: 0.022,
            st.session_state.education.AdvancedDegree: 0.016
        }

    if 'NET_UNEMPLOYMENT_RATE' not in st.session_state:
        st.session_state.NET_UNEMPLOYMENT_RATE = 0.03

    locations = Enum(
            'location', ['Urban', 'Suburban', 'Rural'])
    if 'locations' not in st.session_state:
        st.session_state.locations = locations

    if 'LOCATION_DISTRIBUTION' not in st.session_state:
        st.session_state.LOCATION_DISTRIBUTION = {
            st.session_state.locations.Urban: 0.25,
            st.session_state.locations.Suburban: 0.50,
            st.session_state.locations.Rural: 0.25
        }

    if 'COL_LOCATION_FACTOR' not in st.session_state:
        st.session_state.COL_LOCATION_FACTOR = {
            st.session_state.locations.Urban: 1.25,
            st.session_state.locations.Suburban: 1.0,
            st.session_state.locations.Rural: 0.75
        }


    if 'DAILY_COL' not in st.session_state:
        st.session_state.DAILY_COL = 70


    if 'NUM_WORKERS' not in st.session_state:
        st.session_state.NUM_WORKERS = 1000


    if 'TAX_RATE' not in st.session_state:
        st.session_state.TAX_RATE = 0.20