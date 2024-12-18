import dash
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
from database import fetch_data  # Ensure fetch_data fetches data correctly

# Register the Producers page
dash.register_page(__name__, name="Producers")

# Fetch Data from the database
try:
    producers_data = fetch_data('producers')  # Fetch data from the 'producers' table
    if producers_data:
        # Create DataFrame using exact column names from pgAdmin
        producers_df = pd.DataFrame(producers_data, columns=["name", "address", "contact_information", "current_balance"])
    else:
        # Fallback empty DataFrame if no data
        producers_df = pd.DataFrame(columns=["name", "address", "contact_information", "current_balance"])
except Exception as e:
    producers_df = pd.DataFrame(columns=["name", "address", "contact_information", "current_balance"])
    print(f"Database error: {e}")

# Layout for Producers Page
layout = html.Div([
    html.H1("Producers Information", className="text-center my-4 text-light"),

    # Search Bar
    html.Div([
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Search producers...',
            debounce=True,
            className='form-control mb-3',
            style={'width': '50%', 'margin': 'auto'}
        )
    ], className='text-center'),

    # Data Table
    html.Div([
        dash_table.DataTable(
            id='producers-table',
            columns=[
                {"name": "Name", "id": "name"},
                {"name": "Address", "id": "address"},
                {"name": "Contact Information", "id": "contact_information"},
                {"name": "Current Balance", "id": "current_balance"}
            ],
            data=producers_df.to_dict('records'),
            style_table={'height': '400px', 'overflowY': 'auto'},
            style_cell={
                'textAlign': 'center',
                'padding': '10px',
                'color': '#FFF',
                'backgroundColor': '#222'
            },
            style_header={'backgroundColor': '#333', 'fontWeight': 'bold'}
        )
    ]) if not producers_df.empty else html.P("No data available for producers.", className="text-center text-light")
])


# Callback for Search Filtering
@dash.callback(
    Output('producers-table', 'data'),
    Input('search-input', 'value'),
    prevent_initial_call=False
)
def update_table(search_value):
    """
    Dynamically filter producers data based on search input.
    """
    if not search_value:
        return producers_df.to_dict('records')  # Return all data if search is empty

    # Filter rows where any column matches the search input (case-insensitive)
    filtered_df = producers_df[
        producers_df.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)
    ]
    return filtered_df.to_dict('records')
