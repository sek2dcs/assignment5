# importing packages 
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd 

# reading in csv
data = pd.read_csv("https://github.com/sek2dcs/assignment5/blob/main/gdp_pcap.csv", on_bad_lines = 'skip')
data = data.reset_index()

# using panadas melt function to try to get the columns to be country, year, and gdp per capita
# so it is easier to code the app
data_fixed = pd.melt(data, id_vars='country', var_name='year', value_name='gdp_per_capita')

# converting year and gdp_per_capita columns to integers
# year first...
data_fixed['year'] = data_fixed['year'].astype(int)

# gdp_per_capita has some values that are k instead of 1,0000 
# getting the values that have the 'k' at the end then converting them to floats (bc demicals)
data_fixed.loc[data_fixed['gdp_per_capita'].str.endswith('k', na = False), 'gdp_per_capita'] = data_fixed.loc[data_fixed['gdp_per_capita'].str.endswith('k', na = False), 'gdp_per_capita'].str.rstrip('k').astype(float) * 1000
# now converting the rest of the gdp_per_capita to floats 
data_fixed['gdp_per_capita'] = data_fixed['gdp_per_capita'].astype(float) 

# making filtered df of unique years for slider marks 
# have to make into integers so that the filtered_years works (to be divisble by 100)
unique_years = sorted([int(year) for year in data_fixed['year'].unique()])

# then making list of years by 100 by saying that put the year in this list if it is divisible by 100 
filtered_years = [year for year in unique_years if year % 100 == 0]

# creating dictionary of the diff years 
slider_marks = {year: str(year) for year in filtered_years}

# initializing app 
app = Dash(__name__)
server = app.server

# building app 
app.layout = html.Div([
    html.H1(children = "Gapminder - GDP per capita from 1800-2100"), # title   (below is the paragraph -- in the second div)
    html.Div(children = "This dataset is from Gapminder's estimates of GDP per capita for almost all countries in the world from 18000 to 2100. The creators of this dataset were able to make the GDPs of each country on the same 'scale' by standardizing using a World Bank indicator. Depending on the year, Gapminder had different methods on how to estimate the GDP per capita for each country. Additionally, Syria did not have any official GDP per capita estimate since 2010, so Gapminder estimated these values. This app has a multi-select dropdown where the user can select multiple countries, a range slider for the years in the dataset, and a line graph displaying the gdp per captia for each country from 1800-2100."),
    html.Div([
    html.Div(
        dcc.Dropdown(
            options = [{'label': country, 'value': country} for country in data_fixed.country.unique()], # this gives the dropdown options as the diff countries in the country column of df
            id = "dropdown-country", 
            multi = True, 
            value = ['UK', 'Angola']
        ), className = "six columns",  # makes it so it takes up half (6/12)
    ), 
    html.Div(
        dcc.RangeSlider(min = 1800, max = 2100, id = 'range-slide-yr', 
                        value = [1800, 1900], 
                        marks = slider_marks, # markers for every 100 yrs 
                         tooltip = {'placement' : 'bottom', 'always_visible': True}), # makes it so that the user can see the specific year selected on slider range
        className = "six columns" # makes it so it takes up half (6/12)
    )
], className = "row"), # puts the slider & dropdown on one row 
html.Div([      # another parent div for the line graph 
    dcc.Graph(id = 'line-graph'
    )
])
])


# defining callback
@app.callback(
    Output('line-graph', 'figure'), # outputs will be the line graph 
    [Input('dropdown-country', 'value'), # inputs are the dropdowns & the range slider 
     Input('range-slide-yr', 'value')]
)
def update_fig(selected_country, selected_year): # defining function as update_fig
    dff = data_fixed[(data_fixed['year'] >= selected_year[0]) & (data_fixed['year'] <= selected_year[1]) & (data_fixed['country'].isin(selected_country))]
    # making dff which filters for the selected year min & max from the slider and the selcted countries from the dropdown ^ 
    fig = px.line(dff, x='year', # making line graph! 
                  y= 'gdp_per_capita',
                  color = 'country', title = "year vs gdp per capita per selected countries")
    fig.update_xaxes(title = "year") # titling the axes 
    fig.update_yaxes(title = 'gdp per capita')
    fig.update_layout(transition_duration=500) # doing some animation 

    return fig

# running app
if __name__ == '__main__':
    app.run_server(debug=True)
