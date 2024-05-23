import streamlit as st
from streamlit_option_menu import option_menu

from predict_page import show_predict_page
from explore_page import show_explore_page


with st.sidebar:
    selected = option_menu('Main Menu', ['Salary Prediction', 'Salary Viz'], 
        icons=['cash-coin', 'graph-up'], menu_icon="cast", default_index=1,
        styles={
        "container": {"padding": "0!important", "background-color": "#f0f2f6"},
        "icon": {"color": "black", "font-size": "20px"}, 
        "nav-link": {"font-size": "20px", "text-align": "middle", "margin":"0px", "--hover-color": "#91e7cd"}, 
        "nav-link-selected": {"color": "#ffffff", "background-color": "#147649", "font-weight": "200", "font-size": "20px"},
    }
    )
    

if selected == "Salary Prediction":
    show_predict_page()
else:
    show_explore_page()