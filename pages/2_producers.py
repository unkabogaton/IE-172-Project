import dash
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
from database import fetch_data  # Ensure fetch_data fetches data correctly

# Register the Producers page
dash.register_page(__name__, name="Producers")

# Initial empty DataFrame for layout setup
producers_df = pd.DataFrame(columns=["name", "address", "contact_information", "current_balance"])

# Layout for Producers Page
layout = html.Div([
    html.H1("Producers Information", className="text-center my-4 text-light"),

    # Search Bar
    html.Div([
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Search producers...',
            debounce=False,
            className='form-control mb-3',
            style={'width': '50%', 'margin': 'auto'}
        )
    ], className='text-center'),

    # Message when no results or empty search
    html.Div(id='no-results-message', className="text-center text-light my-4"),

    # Data Table Wrapper
    html.Div(
        id='table-container',  # Wrapper Div for visibility control
        children=[
            dash_table.DataTable(
                id='producers-table',
                columns=[
                    {"name": "Name", "id": "name"},
                    {"name": "Address", "id": "address"},
                    {"name": "Contact Information", "id": "contact_information"},
                    {"name": "Current Balance", "id": "current_balance"}
                ],
                data=[],  # Initial empty data
                style_table={'height': '400px', 'overflowY': 'auto'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'color': '#FFF',
                    'backgroundColor': '#222'
                },
                style_header={'backgroundColor': '#333', 'fontWeight': 'bold'}
            )
        ],
        style={"display": "none"}  # Initially hidden
    )
])


# Callback for Search Filtering
@dash.callback(
    [Output('producers-table', 'data'),
     Output('no-results-message', 'children'),
     Output('table-container', 'style')],
    Input('search-input', 'value'),
    prevent_initial_call=False
)
def update_table(search_value):
    """
    Dynamically filter producers data based on search input.
    """
    if not search_value:
        # No search input: Hide the table and show the default message
        return [], "Search for producers to view their details", {"display": "none"}

    # Fetch filtered data from the database
    try:
        producers_data = fetch_data(
            "producers", 
            conditions=f"name ILIKE '%{search_value}%'"
        )
        print(producers_data)
        if not producers_data:
            # No matches found: Hide the table and show the no-results message
            return [], "No producers match your search.", {"display": "none"}
        
        # Convert to DataFrame
        filtered_df = pd.DataFrame(producers_data, columns=["name", "address", "contact_information", "current_balance"])
        return filtered_df.to_dict('records'), "", {"display": "block"}  # Show the table
    except Exception as e:
        print(f"Database error: {e}")
        return [], "An error occurred while fetching data.", {"display": "none"}
