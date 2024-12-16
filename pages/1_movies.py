import dash
from dash import dcc, html

dash.register_page(__name__, name='Movies')

layout = html.Div(
    [
        # Add a header for the Movies page
        html.H1(
            "Explore Our Movie Listings", 
            className="text-light fw-bold fs-1 text-center", 
            style={'margin-bottom': '20px'}
        ),

        # Movie description text (can be adjusted)
        html.P(
            "<movie listings with description, prod year, awards won, etc.>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),

        # First Row with Search Bar
        html.Div(
            [
                # Search input field with rounded corners
                dcc.Input(
                    id='movie-search', 
                    type='text', 
                    placeholder='Search for a movie...', 
                    style={
                        'width': '80%', 
                        'padding': '10px', 
                        'borderRadius': '15px',  # Rounded corners for input
                        'border': '1px solid #ccc'  # Optional: Border styling
                    }
                ),
                
                # Search button with rounded corners
                html.Button(
                    'Search', 
                    id='search-button', 
                    n_clicks=0, 
                    style={
                        'padding': '10px', 
                        'margin-left': '10px', 
                        'borderRadius': '15px',  # Rounded corners for button
                        'border': '1px solid #ccc'  # Optional: Border styling
                    }
                ),
            ],
            style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px'}
        ),
    ]
)
