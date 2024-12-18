import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import webbrowser

app = dash.Dash(__name__, title='Sineflix Movie Theater', use_pages=True, external_stylesheets=[dbc.themes.SLATE])

# Sidebar setup
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2 text-light"),
            ],
            href=page["path"],
            active="exact",
            className="text-light py-4"
        )
        for page in dash.page_registry.values()
    ],
    pills=True,
    vertical=True,
    className="border border-primary rounded",  # Dark background for the Slate theme
)

# Layout setup
app.layout = dbc.Container([
    dbc.Row([ 
        dbc.Col([html.Img(src='assets/logo.png', height="80px")], 
        ),
    ], className='bg-primary mb-4 mx-1 p-1 rounded-3', style={'height': '90px '}),

    dbc.Row(
        [
            dbc.Col([sidebar], width=2),
            dbc.Col([dash.page_container], width=10)
        ]
    )
], fluid=True)

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050', autoraise=True)
    app.run_server()
