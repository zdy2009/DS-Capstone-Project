import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1: Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard",
            style={'color': '#503D36', 'font-size': '24px', 'text-align': 'center'}),

    # TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),

    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': str(year), 'value': year} for year in year_list],
        value='Select Year',
        disabled=True
    )),

    # TASK 2.3: Add a division for output display
    html.Div([
        html.Div(id='output-container', className='chart-grid',
                 style={'display': 'flex'})
    ])
])


# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
# Callback to enable or disable the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True


# Callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year wise) using line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                           x='Year',
                           y='Automobile_Sales',
                           title="Average Automobile Sales fluctuation over Recession Period")
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          title="Average Vehicles Sold by Vehicle Type during Recession")
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                          values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title="Total Advertisement Expenditure by Vehicle Type during Recession")
        )

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        unemployment_effect = recession_data.groupby('Vehicle_Type')[
            ['unemployment_rate', 'Automobile_Sales']].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemployment_effect,
                          x='Vehicle_Type',
                          y='unemployment_rate',
                          title="Effect of Unemployment Rate on Vehicle Type during Recession")
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)])
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year and input_year != 'Select Year':
        yearly_data = data[data['Year'] == int(input_year)]

        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yearly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yearly_sales,
                           x='Month',
                           y='Automobile_Sales',
                           title="Yearly Automobile Sales for {}".format(input_year))
        )

        # Plot 2: Total Monthly Automobile sales using line chart
        Y_chart2 = dcc.Graph(
            figure=px.line(yearly_sales,
                           x='Month',
                           y='Automobile_Sales',
                           title="Total Monthly Automobile Sales for {}".format(input_year))
        )

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        average_vehicles_sold = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(average_vehicles_sold,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          title="Average Vehicles Sold by Vehicle Type for {}".format(input_year))
        )

        # Plot 4: Pie chart for total advertisement expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                          values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title="Total Advertisement Expenditure by Vehicle Type for {}".format(input_year))
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)])
        ]

    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
