from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd 
import requests

url = "https://github.com/sek2dcs/assignment5/raw/main/data_fixed.csv"
response = requests.get(url)
with open("data_fixed.csv", "wb") as f:
    f.write(response.content)

data_fixed = pd.read_csv("data_fixed.csv")
data_fixed = data_fixed.reset_index()

unique_years = sorted([int(year) for year in data_fixed['year'].unique()])

filtered_years = [year for year in unique_years if year % 100 == 0]

slider_marks = {year: str(year) for year in filtered_years}
 
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1(children = "Gapminder - GDP per capita from 1800-2100"),
    html.Div(children = "This dataset is from Gapminder's estimates of GDP per capita for almost all countries in the world from 18000 to 2100. The creators of this dataset were able to make the GDPs of each country on the same 'scale' by standardizing using a World Bank indicator. Depending on the year, Gapminder had different methods on how to estimate the GDP per capita for each country. Additionally, Syria did not have any official GDP per capita estimate since 2010, so Gapminder estimated these values. This app has a multi-select dropdown where the user can select multiple countries, a range slider for the years in the dataset, and a line graph displaying the gdp per captia for each country from 1800-2100."),
    html.Div([
        html.Div([
            dcc.Dropdown(
                options = [{'label': country, 'value': country} for country in data_fixed.country.unique()], 
                id = "dropdown-country", 
                multi = True, 
                value = ['UK', 'Angola']
            )
        ], className="col-md-6"), 
        html.Div([
            dcc.RangeSlider(min = 1800, max = 2100, id = 'range-slide-yr', 
                            value = [1800, 1900], 
                            marks = slider_marks,
                            tooltip = {'placement' : 'bottom', 'always_visible': True})
        ], className="col-md-6")
    ], className = "row"),
    html.Div([    
        dcc.Graph(id = 'line-graph')
    ])
])


@app.callback(
    Output('line-graph', 'figure'), 
    [Input('dropdown-country', 'value'), 
     Input('range-slide-yr', 'value')]
)
def update_fig(selected_country, selected_year): 
    dff = data_fixed[(data_fixed['year'] >= selected_year[0]) & (data_fixed['year'] <= selected_year[1]) & (data_fixed['country'].isin(selected_country))]
    fig = px.line(dff, x='year', 
                  y= 'gdp_per_capita',
                  color = 'country', title = "year vs gdp per capita per selected countries")
    fig.update_xaxes(title = "year") 
    fig.update_yaxes(title = 'gdp per capita')
    fig.update_layout(transition_duration=500) 

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
