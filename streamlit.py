import streamlit as st


# loads all of the necessary constants
import constants
    

constants.init()   
   
st.title('Labor Market Simulator')


col1, col2, col3 = st.columns(3)

with col1:
    st.write('By: Maksim Sviridov')

with col2:
    st.page_link('https://github.com/sviridovm', label='GitHub')
    
with col3:
    st.page_link('https://sviridovm.github.io/', label='Website')
    

pg = st.navigation([st.Page('options.py'), st.Page('simulation.py')])
pg.run()
