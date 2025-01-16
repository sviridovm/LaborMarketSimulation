import streamlit as st


# Streamlit page
st.title("Simulation Constants Configuration")

st.header("General Settings")

new_num_workers = st.number_input(
    "Number of Workers (default: 1000)",
    value=st.session_state.NUM_WORKERS,
    min_value=0,
    step=10
)


new_tax_rate = st.number_input(
    "Tax Rate (default: 0.20)",
    value=st.session_state.TAX_RATE,
    min_value=0.0,
    max_value=0.25,
)

st.header("Education Distribution")
new_education_distribution = {}
total_education_prob = 0
for edu in st.session_state.education:
    prob = st.number_input(
        f"{edu.name} Probability (default: {st.session_state.EDUCATION_DISTRIBUTION[edu]})",
        value=st.session_state.EDUCATION_DISTRIBUTION[edu],
        min_value=0.0,
        max_value=1.0,
        step=0.01
    )
    new_education_distribution[edu] = prob
    total_education_prob += prob

if total_education_prob != 1.0:
    st.error(f"Education probabilities must sum to 1. Current sum: {total_education_prob:.2f}")

st.header("Median Earnings by Education")
new_median_earnings = {}
for edu in st.session_state.education:
    earning = st.number_input(
        f"{edu.name} Median Earning (default: {st.session_state.MEDIAN_EARNING_BY_EDUCATION[edu]})",
        value=st.session_state.MEDIAN_EARNING_BY_EDUCATION[edu],
        min_value=0,
        step=1000
    )
    new_median_earnings[edu] = earning

st.header("Unemployment Rate by Education")
new_unemployment_rate = {}
for edu in st.session_state.education:
    rate = st.number_input(
        f"{edu.name} Unemployment Rate (default: {st.session_state.UNEMPLOYMENT_RATE_BY_EDUCATION[edu]})",
        value=st.session_state.UNEMPLOYMENT_RATE_BY_EDUCATION[edu],
        min_value=0.0,
        max_value=1.0,
        step=0.001
    )
    new_unemployment_rate[edu] = rate

st.header("Location Distribution")
new_location_distribution = {}
total_location_prob = 0
for loc in st.session_state.locations:
    prob = st.number_input(
        f"{loc.name} Probability (default: {st.session_state.LOCATION_DISTRIBUTION[loc]})",
        value=st.session_state.LOCATION_DISTRIBUTION[loc],
        min_value=0.0,
        max_value=1.0,
        step=0.01
    )
    new_location_distribution[loc] = prob
    total_location_prob += prob

if total_location_prob != 1.0:
    st.error(f"Location probabilities must sum to 1. Current sum: {total_location_prob:.2f}")

st.header("Cost of Living Factors")
new_col_location_factor = {}
for loc in st.session_state.locations:
    factor = st.number_input(
        f"{loc.name} Cost of Living Factor (default: {st.session_state.COL_LOCATION_FACTOR[loc]})",
        value=st.session_state.COL_LOCATION_FACTOR[loc],
        min_value=0.0,
        step=0.01
    )
    new_col_location_factor[loc] = factor

new_daily_col = st.number_input(
    "Daily Cost of Living (default: $70)",
    value=st.session_state.DAILY_COL,
    min_value=0,
    step=1
)



# Button to confirm changes
if st.button("Apply Changes"):
    if total_education_prob == 1.0 and total_location_prob == 1.0:
        st.session_state.EDUCATION_DISTRIBUTION.update(new_education_distribution)
        st.session_state.MEDIAN_EARNING_BY_EDUCATION.update(new_median_earnings)
        st.session_state.UNEMPLOYMENT_RATE_BY_EDUCATION.update(new_unemployment_rate)
        st.session_state.LOCATION_DISTRIBUTION.update(new_location_distribution)
        st.session_state.COL_LOCATION_FACTOR.update(new_col_location_factor)
        st.session_state.DAILY_COL = new_daily_col
        
        st.session_state.SIMULATION_READY = False
        
        if 'labor_market' in st.session_state:      
            del st.session_state.labor_market
        
        st.success("Changes applied successfully!")
    else:
        st.error("Fix the probability sums before applying changes.")