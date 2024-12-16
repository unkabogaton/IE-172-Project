import dash
from dash import dcc, html
import plotly.graph_objects as go

dash.register_page(__name__, name="Reports")

# Mock Data
top_movies = [
    {"title": "Top Gun: Maverick", "rating": "8.3", "description": "High-flying action sequel."},
    {"title": "Oppenheimer", "rating": "8.8", "description": "Historical drama about the atomic bomb."},
    {"title": "The Batman", "rating": "8.2", "description": "Dark, gritty superhero story."},
    {"title": "Everything Everywhere All at Once", "rating": "8.1", "description": "Multiverse-spanning adventure."},
]
ticket_sales = [5000, 4500, 3000, 4000]
annual_expenses = [100000, 120000, 110000, 105000]
annual_revenues = [200000, 220000, 210000, 215000]
new_members = [300, 320, 310, 340]

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
expenses_revenue_chart.add_trace(go.Bar(x=["2021", "2022", "2023", "2024"], y=annual_expenses, name="Expenses"))
expenses_revenue_chart.add_trace(go.Bar(x=["2021", "2022", "2023", "2024"], y=annual_revenues, name="Revenue"))
expenses_revenue_chart.update_layout(
    title="Annual Expenses vs. Revenues",
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
    title="New Members per Quarter",
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
                dcc.Tab(label='Top Movies', value='tab-1'),
                dcc.Tab(label='Ticket Sales Analysis', value='tab-2'),
                dcc.Tab(label='Statistics & Graphs', value='tab-3'),
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
                                html.H4(movie["title"], className="text-light fw-bold"),
                                html.P(f"Rating: {movie['rating']}", className="text-muted"),
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
                html.H2("Statistics, Graphs & Data Analysis", className="text-light fw-bold fs-3 text-center"),

                # Annual Expenses vs. Revenues Chart
                html.Div(
                    [
                        html.H3("Annual Expenses vs. Revenues", className="text-light fw-bold fs-4 text-center"),
                        dcc.Graph(figure=expenses_revenue_chart),
                    ],
                    style={'margin-bottom': '20px'}
                ),

                # New Members Chart
                html.Div(
                    [
                        html.H3("New Members per Quarter", className="text-light fw-bold fs-4 text-center"),
                        dcc.Graph(figure=new_members_chart),
                    ]
                ),
            ],
            style={'margin-bottom': '20px'}
        )
