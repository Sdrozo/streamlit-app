# Streamlit live coding script
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from copy import deepcopy


# First some MPG Data Exploration
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

internet_df_raw = load_data(path=".\data\share-of-individuals-using-the-internet.csv")
internet_df = deepcopy(internet_df_raw)

#preset values for the two countries
Entity1 = 'Switzerland'
Entity2 = 'United Kingdom'

# Add title and header
st.title("Internet Usage per Country")
st.header("Map")

# Setting up columns
left_column, middle_column, right_column = st.columns([1, 1, 1])

# Widgets: selectbox
years = sorted(pd.unique(internet_df['Year']))
year = left_column.selectbox("Choose a Year", years)

reduced_df = internet_df[internet_df["Year"] == year]

# Sample Choropleth mapbox using Plotly GO
st.subheader(f"Individuals using the Internet (% of population) for the year {year}")

#C:\Users\sebas\Documents\Constructor Academy\streamlit-app\data\countries.geojson

with open(".\data\countries.geojson") as response:
    countries = json.load(response)

fig1 = px.choropleth(
    reduced_df,
    geojson=countries,
    locations='Code',
    featureidkey="properties.ISO_A3",  # Adjust based on your GeoJSON structure
    color='Individuals using the Internet (% of population)',
    color_continuous_scale='thermal',
    labels={'Individuals using the Internet (% of population)': 'Internet Users (%)'},
    hover_data=['Entity', 'Code', 'Individuals using the Internet (% of population)']
)

fig1.update_geos(projection_type="natural earth")
fig1.update_layout(mapbox_style="carto-positron", mapbox_zoom=3, mapbox_center={"lat": 37.0902, "lon": -95.7129})

st.plotly_chart(fig1)

st.subheader('Internet Users Over Time Comparison')


# Widgets: selectbox
Entities = pd.unique(internet_df['Entity'])
Entity1 = middle_column.selectbox("Choose the first country", Entities)
Entity2 = right_column.selectbox("Choose the second country", Entities)

reduced_df1 = internet_df[internet_df["Entity"] == Entity1]
reduced_df2 = internet_df[internet_df["Entity"] == Entity2]

# Create separate Scatter traces for each entity with hover text
trace1 = go.Scatter(
    x=reduced_df1['Year'],
    y=reduced_df1['Individuals using the Internet (% of population)'],
    name=Entity1,
    mode='lines+markers',  # Show both lines and markers
    text=[f'{Entity1}<br>Year: {year}<br>Internet Users (%): {percentage}' 
          for year, percentage in zip(reduced_df1['Year'], reduced_df1['Individuals using the Internet (% of population)'])]
)

trace2 = go.Scatter(
    x=reduced_df2['Year'],
    y=reduced_df2['Individuals using the Internet (% of population)'],
    name=Entity2,
    mode='lines+markers',
    text=[f'{Entity2}<br>Year: {year}<br>Internet Users (%): {percentage}' 
          for year, percentage in zip(reduced_df2['Year'], reduced_df2['Individuals using the Internet (% of population)'])]
)

# Create the figure with the list of traces
fig2 = go.Figure([trace1, trace2])

st.plotly_chart(fig2)

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=internet_df)
    # st.table(data=mpg_df)