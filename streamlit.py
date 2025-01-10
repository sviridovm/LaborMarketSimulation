import streamlit as st


# loads all of the necessary constants
import constants
    

constants.init()   
   
st.title('Labor Market Simulator')


pg = st.navigation([st.Page('options.py'), st.Page('simulation.py')])
pg.run()
    