# importing packages 
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd 
import requests

# using the requests library to access the data that i reformatted in assignment 4 (using pd.melt)
url = "https://github.com/sek2dcs/assignment5/raw/main/data_fixed.csv"
response = requests.get(url)
with open("data_fixed.csv", "wb") as f:
    f.write(response.content)

# reading the data in & resetting index just for debugging efforts
data_fixed = pd.read_csv("data_fixed.csv")
data_fixed = data_fixed.reset_index()

# making filtered df of unique years for slider marks 
# have to make into integers so that the filtered_years works (to be divisble by 100)
unique_years = sorted([int(year) for year in data_fixed['year'].unique()])

# then making list of years by 100 by saying that put the year in this list if it is divisible by 100 
filtered_years = [year for year in unique_years if year % 100 == 0]

# creating dictionary of the diff years 
slider_marks = {year: str(year) for year in filtered_years}

# loading in stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] 

# initializing app 
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

# building app
app.layout = html.Div([
    html.H1(children = "Gapminder - GDP per capita from 1800-2100"),     # title   (below is the paragraph -- in the second div)
    html.Div(children = "This dataset is from Gapminder's estimates of GDP per capita for almost all countries in the world from 18000 to 2100. The creators of this dataset were able to make the GDPs of each country on the same 'scale' by standardizing using a World Bank indicator. Depending on the year, Gapminder had different methods on how to estimate the GDP per capita for each country. Additionally, Syria did not have any official GDP per capita estimate since 2010, so Gapminder estimated these values. This app has a multi-select dropdown where the user can select multiple countries, a range slider for the years in the dataset, and a line graph displaying the gdp per captia for each country from 1800-2100."),
    html.Div([
        html.Div([
            dcc.Dropdown(
                options = [{'label': country, 'value': country} for country in data_fixed.country.unique()], # this gives the dropdown options as the diff countries in the country column of df
                id = "dropdown-country", 
                multi = True, 
                value = ['UK', 'Angola']
            )
        ], style={'width': '48%', 'display': 'inline-block'}), # makes it so it takes up half (6/12)
        html.Div([
            dcc.RangeSlider(min = 1800, max = 2100, id = 'range-slide-yr', 
                            value = [1800, 1900], 
                            marks = slider_marks,  # markers for every 100 yrs 
                            tooltip = {'placement' : 'bottom', 'always_visible': True}) 
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}) # makes it so it takes up half (6/12)
    ], className = "row"), # puts the slider & dropdown on one row 
    html.Div([    
        dcc.Graph(id = 'line-graph')
])
])

# defining callback 
@app.callback(
    Output('line-graph', 'figure'),     # outputs will be the line graph 
    [Input('dropdown-country', 'value'), # inputs are the dropdowns & the range slider 
     Input('range-slide-yr', 'value')]
)
def update_fig(selected_country, selected_year): # defining function as update_fig
    dff = data_fixed[(data_fixed['year'] >= selected_year[0]) & (data_fixed['year'] <= selected_year[1]) & (data_fixed['country'].isin(selected_country))]
      # making dff which filters for the selected year min & max from the slider and the selcted countries from the dropdown ^ 
    fig = px.line(dff, x='year',  # making line graph! 
                  y= 'gdp_per_capita',
                  color = 'country', title = "year vs gdp per capita per selected countries")
    fig.update_xaxes(title = "year") # titling the axes 
    fig.update_yaxes(title = 'gdp per capita')
    fig.update_layout(transition_duration=500) # doing some animation 

    return fig

# running app
if __name__ == '__main__':
    app.run_server(debug=True)
