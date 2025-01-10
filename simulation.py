import streamlit as st
import pandas as pd
from labor_market import LaborMarket

if not st.session_state.get('SIMULATION_READY', False):
        st.write('Make sure to adjust values before starting simulation')
        
        if st.button('Ready to Simulate'):
            st.session_state.SIMULATION_READY = True
            st.rerun()

else:    

        
        working_population = 1000
        if 'labor_market' not in st.session_state:            
            st.session_state.labor_market = LaborMarket(working_population)



        workers_df = pd.DataFrame(
            [worker.display() for worker in st.session_state.labor_market.get_workers()],
            columns=['Education Level', 'Salary', 'Location', 'Cost of Living in USD ($)', 'Savings in USD ($)' , 'Employed', 'Job ID']
        )


        with st.expander('Worker Data'):
            # st.write(workers_df)
            st.dataframe(workers_df)




        metrics_df = pd.DataFrame(
            {
                'Average Salary': st.session_state.labor_market.metrics.avg_salaries, 
                'Average COL': st.session_state.labor_market.metrics.avg_COL 
            }
        )


        employment_df = pd.DataFrame(
            {
                'Unemployment Rate': st.session_state.labor_market.metrics.unemployment_rate
            }
        )


        with st.container(border=True):
            st.title('Metrics')
            
            with st.expander('Average Salary and Cost of Living'):
                st.line_chart(metrics_df)
            
            with st.expander('Unemployment Rate'):
                st.line_chart(employment_df)    
            


        st.button('Simulate', on_click=st.session_state.labor_market.simulate)


        # print(dir(st.session_state.labor_market)) 

        num_employed = st.session_state.labor_market.employed_worker_count
        st.write(f'Number of employed workers: {num_employed}')
        open_job_count = st.session_state.labor_market.open_job_count
        st.write(f'Number of open jobs: {open_job_count}')


        # make a drop down which shows the salary history for each worker by id
        worker_id = st.selectbox('Select a worker ID', workers_df.index)
        worker = st.session_state.labor_market.get_workers()[worker_id]

        st.write(f'Salary history for worker {worker_id}')
        st.line_chart(worker.salary_history, y_label='Salary')

