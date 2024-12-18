import dash
from dash import dcc, html

import plotly.graph_objects as go

import pandas as pd

from database import fetch_data

dash.register_page(__name__, name="Reports")

# Mock Data


reports = fetch_data('reports')
top_movies = fetch_data('movies', '*', None, 'ratings', 'DESC', 4)

reports_df = pd.DataFrame(reports)

years = reports_df['year'].tolist()
annual_revenues = reports_df['annual_revenue'].tolist()
new_members = reports_df['new_members'].tolist()
annual_expenses = reports_df['annual_expenses'].tolist()


ticket_sales = [5000, 4500, 3000, 4000]


# Common Theme for Charts
chart_theme = {
    "plot_bgcolor": "#333333",
    "paper_bgcolor": "#333333",
    "font": {"color": "#FFFFFF"}
}

# Ticket Sales Chart
ticket_sales_chart = go.Figure(
    go.Bar(
        x=[movie["title"] for movie in top_movies],
        y=ticket_sales,
        marker_color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
    )
)
ticket_sales_chart.update_layout(
    title="Ticket Sales by Movie",
    xaxis_title="Movies",
    yaxis_title="Tickets Sold",
    height=300,
    margin=dict(t=40, b=40),
    **chart_theme
)

# Annual Expenses vs. Revenues Chart
expenses_revenue_chart = go.Figure()
expenses_revenue_chart.add_trace(go.Bar(x=years, y=annual_expenses, name="Expenses"))
expenses_revenue_chart.add_trace(go.Bar(x=years, y=annual_revenues, name="Revenue"))
expenses_revenue_chart.update_layout(
    # title="Annual Expenses vs. Revenues",
    xaxis_title="Year",
    yaxis_title="Amount ($)",
    barmode="group",
    height=300,
    margin=dict(t=40, b=40),
    **chart_theme
)

# New Members Chart
new_members_chart = go.Figure(
    go.Scatter(
        x=["Q1", "Q2", "Q3", "Q4"],
        y=new_members,
        marker=dict(color="#9467bd"),
        mode="lines+markers",
    )
)
new_members_chart.update_layout(
    # title="New Members per Quarter",
    xaxis_title="Quarter",
    yaxis_title="Number of New Members",
    height=300,
    margin=dict(t=40, b=40),
    **chart_theme
)

# Layout with Tabs
layout = html.Div(
    [
        # Header
        html.H1(
            "Reports Overview",
            className="text-light fw-bold fs-1 text-center",
            style={'margin-bottom': '20px'}
        ),

        # Tabs
        dcc.Tabs(
            id="reports-tabs",
            value='tab-1',
            children=[
                dcc.Tab(label='Top Movies', value='tab-1', style={"color": "#808080"}),
                dcc.Tab(label='Ticket Sales Analysis', value='tab-2', style={"color": "#808080"}),
                dcc.Tab(label='Statistics & Graphs', value='tab-3', style={"color": "#808080"}),
            ],
            style={"background-color": "#333333", "color": "#FFFFFF"},
        ),

        # Tab Content
        html.Div(id='reports-tabs-content', className="text-light")
    ]
)

# Callback to update tab content
@dash.callback(
    dash.Output('reports-tabs-content', 'children'),
    [dash.Input('reports-tabs', 'value')]
)
def render_tab_content(tab):
    if tab == 'tab-1':
        return html.Div(
            [
                html.H2("Top Movies", className="text-light fw-bold fs-3 text-center"),
                html.Div(
                    [
                        html.Div(
                            [
                                 html.Img(
                                    src=movie["link_to_pictures"],
                                    alt=movie["title"], 
                                    className="img-fluid mb-3", 
                                    style={"width": "100%", "height": "auto"}
                                ),
                                html.H4(movie["title"], className="text-light fw-bold"),
                                html.P(f"Rating: {movie['ratings']}", className="text-muted"),
                                html.P(movie["description"], className="text-light"),
                            ],
                            className="border border-light rounded p-3 mb-3",
                            style={"width": "22%", "display": "inline-block", "margin": "10px"},
                        )
                        for movie in top_movies
                    ],
                    style={"text-align": "center"}
                ),
            ],
            style={'margin-bottom': '20px'}
        )
    elif tab == 'tab-2':
        return html.Div(
            [
                html.H2("Ticket Sales Analysis", className="text-light fw-bold fs-3 text-center"),
                dcc.Graph(figure=ticket_sales_chart),
            ],
            style={'margin-bottom': '20px'}
        )
    elif tab == 'tab-3':
        return html.Div(
            [
                html.H2("Statistics, Graphs & Data Analysis", className="text-light fw-bold fs-3 text-center",  
                    style={
                        'margin': '20px'
                        }),

                # Annual Expenses vs. Revenues Chart
                html.Div(
                    [
                        html.H3("Annual Expenses vs. Revenues", className="text-light fw-bold fs-4 text-center", style={'margin-bottom': '5px'}),
                        dcc.Graph(figure=expenses_revenue_chart,  style={'margin': '20px', 'padding': '20px'}),
                    ],
                    style={'margin-bottom': '20px', 'padding': '10px'}
                ),

                # New Members Chart
                html.Div(
                    [
                        html.H3("New Members per Quarter", className="text-light fw-bold fs-4 text-center", style={'margin-bottom': '5px'}),
                        dcc.Graph(figure=new_members_chart, style={'margin': '20px', 'padding': '20px'}),
                    ]
                ),
            ],
            style={'margin-bottom': '20px', 'padding': '10px'}
        )
