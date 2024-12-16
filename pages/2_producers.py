import dash
from dash import dcc, html

dash.register_page(__name__, name='Producers')

layout = html.Div(
    [
        # Add a header for the Producers page
        html.H1(
            "Meet Our Movie Producers", 
            className="text-light fw-bold fs-1 text-center", 
            style={'margin-bottom': '20px'}
        ),

        # List of producers and details
        html.P(
            "<list of producers, their produced movies and transactions with them>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),
    ]
)
