import dash
from dash import dcc, html

dash.register_page(__name__, name="Updates")

layout = html.Div(
    [
        # Add a header for the User Profile page
        html.H1(
            "User Profile and Settings", 
            className="text-light fw-bold fs-1 text-center", 
            style={'margin-bottom': '20px'}
        ),

        # View/update personal information section
        html.P(
            "<view/ update personal information>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),

        # View transaction history section
        html.P(
            "<view transaction history>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),
    ]
)
