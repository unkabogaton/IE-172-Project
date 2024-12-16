import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__, name="Customers")

df = px.data.tips()

layout = html.Div(
    [
        # Add a header for the Customers page
        html.H1(
            "Customer Information and Purchase History", 
            className="text-light fw-bold fs-1 text-center", 
            style={'margin-bottom': '20px'}
        ),

        # Customer-related information or visualizations
        html.P(
            "<customer information, purchase history, etc.>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),
    ]
)
