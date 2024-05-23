import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import colorcet as cc

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range (len(categories)):
        if categories.values[i] >= cutoff : 
            categorical_map[categories.index[i]] = categories.index[i]
        else :
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_YearsCodePro(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_EdLevel(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x:
        return 'Post Grad'
    return 'Less than a Bachelors'

@st.cache_data
def load_data():
    df = pd.read_csv('survey_results_public.csv')
    df = df[['EdLevel', 'Country', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
    df = df.rename({'ConvertedCompYearly' : 'Salary'}, axis = 1)
    df = df.dropna()
    df = df[df['Employment'] == 'Employed, full-time']
    df = df.drop('Employment', axis=1)
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary'] <= 250000]
    df = df[df['Salary'] >= 10000]
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_YearsCodePro)
    df['EdLevel'] = df['EdLevel'].apply(clean_EdLevel)

    return df

df = load_data()
df['Country'] = df['Country'].replace('United Kingdom of Great Britain and Northern Ireland', 'UK & Ireland')

def show_explore_page():
    st.title("Stack Overflow Developer Survey 2023")

    data = df['Country'].value_counts()

    fig1, ax1 = plt.subplots()
    cmap = cc.glasbey_hv
    ax1.pie(data, labels=data.index
            , autopct = '%1.1f%%'
            , startangle = 90
            , labeldistance = None
            , colors=cmap)
    ax1.axis('equal')
    fig1.legend(ax1.patches
                , data.index
                , loc='upper left'
                , bbox_to_anchor=(1.0, 1.0))
    

    st.write("""#### Number of data from different countries""")
    st.pyplot(fig1)



    st.write("""#### Average Salary Based On Countries""")
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    fig2, ax2 = plt.subplots()
    ax2.bar(data.index, data.values, color=cmap)
    ax2.set_xlabel('Country')
    ax2.set_ylabel('Average Salary')
    ax2.tick_params(axis='x', rotation=90)
    st.pyplot(fig2)



    st.write("""#### Average Salary Based On Experience""")
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
