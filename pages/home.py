import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


dash.register_page(__name__, name='Home', path='/')


tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Now Showing", className="text-light fw-bold fs-1"),            
            # Create a container for the movie cards
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    # Movie Image
                                    html.Img(src="assets/movie1.jpg", alt="Movie 1", className="img-fluid"),

                                    # Movie Name
                                    html.H5("Movie Name 1", className="text-light mt-2"),

                                    # Buy Tickets Button
                                    dbc.Button("Buy Tickets", color="primary", className="mt-2", href="#")
                                ]
                            ),
                            className="mb-4"
                        ),
                        width=3
                    ),
                    
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    # Movie Image
                                    html.Img(src="assets/movie2.jpg", alt="Movie 2", className="img-fluid"),

                                    # Movie Name
                                    html.H5("Movie Name 2", className="text-light mt-2"),

                                    # Buy Tickets Button
                                    dbc.Button("Buy Tickets", color="primary", className="mt-2", href="#")
                                ]
                            ),
                            className="mb-4"
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    # Movie Image
                                    html.Img(src="assets/movie3.jpg", alt="Movie 3", className="img-fluid"),

                                    # Movie Name
                                    html.H5("Movie Name 3", className="text-light mt-2"),

                                    # Buy Tickets Button
                                    dbc.Button("Buy Tickets", color="primary", className="mt-2", href="#")
                                ]
                            ),
                            className="mb-4"
                        ),
                        width=3
                    ),
                    
                    # Add more movie cards as needed
                ],
                className="g-3"  # Grid gap between columns
            ),
        ]
    ),
    className="mt-3",
)


tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Coming Soon", className="text-light fw-bold fs-1"),
            html.P("<movie gallery>", className="text-light fw-bold fs-3"),
        ]
    ),
    className="mt-3",
)

# Defining the tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Now Showing"),
        dbc.Tab(tab2_content, label="Coming Soon"),
    ]
)

login_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Login", className="card-title text-center"),
            dbc.Input(type="text", placeholder="Username", className="mb-3"),
            dbc.Input(type="password", placeholder="Password", className="mb-3"),

            # Centered, smaller submit button
            dbc.Row(
                dbc.Col(
                    dbc.Button("Submit", color="primary", className="mt-3", style={"width": "auto", "padding": "8px 16px", "font-size": "14px"}), 
                    className="d-flex justify-content-center"
                ),
                justify="center"
            ),

            # Centered registration question and link
            dbc.Row(
                [
                    html.P("Don't have an account?", className="mt-3 text-center"),
                    dcc.Link("Register here", href="/register", className="text-light text-center"),
                ],
                justify="center",
                className="mt-3"
            )
        ]
    ),
    className="mt-5"
)


# Defining the layout
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(tabs),
                dbc.Col(login_card, width=3,)
            ]
        )
    ]
)




if __name__ == "__main__":
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = layout
    app.run_server(debug=True)
