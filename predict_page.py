import streamlit as st
import numpy as np
import pickle


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor_loaded = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Dev Salary Prediction")

    st.write("""##### We need some information to predict the salary""")

    countries = (
        "Australia"
        , "Brazil"
        , "Canada"
        , "Denmark"
        , "France"
        , "Germany"
        , "India"
        , "Israel"
        , "Italy"
        , "Netherlands"
        , "Norway"
        , "Poland"
        , "Spain"
        , "Sweden"
        , "United Kingdom of Great Britain and Northern Ireland"
        , "United States of America"
        , 'Other'
    )

    education = (
        "Less than a Bachelors"
        , "Bachelor’s degree"
        , "Master’s degree"
        , "Post Grad"
        )


    country = st.selectbox("Country"
                           , countries
                           , index=None
                           , placeholder="Select your country"
                           ,)

    st.write("You're from ", country)
    

    education = st.selectbox("Education Level"
                             , education
                             , index=None
                             , placeholder="Select your education level"
                             ,)
    
    st.write("Your education level is ", education, ".")
    

    experience = st.slider(
        "Years of Experience"
        , 0, 50, 3
        # "How many years have you gone proffesional as a sofwate developer?"
        )
    st.write("You've been a proffesional sofware developer for ", experience, " years.")

    
    ok = st.button("Calculate your expected salary")
    if ok:
        new_values = np.array([[country, education, experience]])
        new_values[:, 0] = le_country.transform(new_values[:,0])
        new_values[:, 1] = le_education.transform(new_values[:,1])
        new_values = new_values.astype(float)

        salary = regressor_loaded.predict(new_values)
        st.subheader(f"Your estimated salary is ${salary[0]:.2f}", divider = 'green')
