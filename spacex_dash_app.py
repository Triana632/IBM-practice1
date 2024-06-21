# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                            id='site-dropdown',
                                            options=[{'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                            value='ALL',  # Default value is for ALL sites
                                            placeholder='Select a Launch Site here',
                                            searchable=True
                                            ),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.P("Payload range (Kg):"),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Filter data to include all sites
        filtered_df = spacex_df
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    # Create a pie chart
    if selected_site == 'ALL':
        # Summing up the success count for all sites
        fig = px.pie(
            filtered_df, 
            names='class',
            title='Total Success Launches for all Sites'
        )
    else:
        # Showing success vs failure counts for the selected site
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs. Failed Counts for {selected_site}'
        )
    
    return fig

                                
# TASK 3: Add a slider to select payload range
dcc.RangeSlider(
    id='payload-slider',
    min=0,  # Slider starts at 0 Kg
    max=10000,  # Slider ends at 10000 Kg
    step=1000,  # Interval of 1000 Kg between slider steps
    value=[min_payload, max_payload],  # Default selected range from min to max
    marks={i: str(i) for i in range(0, 10001, 1000)}  # Numeric labels for the slider
),

# TASK 4: Add a scatter chart to show the correlation between payload and launch success
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    # Filter by payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) & 
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]

    # Generate the scatter plot
    fig = px.scatter(
        filtered_df, 
        x='Payload Mass (kg)', 
        y='class',
        color='Booster Version Category',
        labels={
            'class': 'Launch Outcome',  # Making sure the label for class is clear
            'Payload Mass (kg)': 'Payload Mass (kg)'
        },
        title=f'Scatter Plot: Payload vs. Launch Outcome for {selected_site if selected_site != "ALL" else "All Sites"}'
    )

    return fig                                
                                

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
