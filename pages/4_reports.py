import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from database import fetch_data

dash.register_page(__name__, name="Reports")

# Fetch Data
reports = fetch_data('reports')
top_movies = fetch_data('movies', '*', None, 'ratings', 'DESC', 4)

# Data Processing
reports_df = pd.DataFrame(reports)
years = reports_df['year'].tolist()
annual_revenues = reports_df['annual_revenue'].tolist()
new_members = reports_df['new_members'].tolist()
annual_expenses = reports_df['annual_expenses'].tolist()

ticket_sales = [5000, 4500, 3000, 4000]

# Common Theme for Dark Aesthetic Charts with Updated Font
chart_theme = {
    "plot_bgcolor": "#000000",  # Black background
    "paper_bgcolor": "#000000",
    "font": {"color": "#FFFFFF", "family": "Poppins, sans-serif"},  # Modern Poppins font
    "title_x": 0.5,  # Center-align titles
    "xaxis": {"showgrid": True, "gridcolor": "#444444", "linecolor": "#FFFFFF"},
    "yaxis": {"showgrid": True, "gridcolor": "#444444", "linecolor": "#FFFFFF"}
}

# Ticket Sales Chart with Updated Colors
ticket_sales_chart = go.Figure()
ticket_sales_chart.add_trace(
    go.Bar(
        x=[movie["title"] for movie in top_movies],
        y=ticket_sales,
        marker=dict(
            color=["#E63946", "#E63946", "#6E6E6E", "#C4C4C4"],  # Red and gray shades
            line=dict(width=0)
        ),
        width=0.5
    )
)
ticket_sales_chart.update_traces(marker_line_width=1, marker_line_color="#FFFFFF")
ticket_sales_chart.update_layout(
    title="Ticket Sales by Movie 🎟️",
    xaxis_title="Movies",
    yaxis_title="Tickets Sold",
    height=350,
    margin=dict(t=60, b=60),
    **chart_theme
)

# Annual Expenses vs Revenues Chart with Updated Colors
expenses_vs_revenues = go.Figure()
expenses_vs_revenues.add_trace(
    go.Bar(
        x=years, y=annual_expenses,
        name="Expenses",
        marker=dict(color="#E63946", opacity=0.8)  # Red
    )
)
expenses_vs_revenues.add_trace(
    go.Bar(
        x=years, y=annual_revenues,
        name="Revenue",
        marker=dict(color="#6E6E6E", opacity=0.8)  # Gray
    )
)
expenses_vs_revenues.update_layout(
    title="Annual Expenses vs. Revenues 💼",
    xaxis_title="Year",
    yaxis_title="Amount ($)",
    barmode="group",
    height=350,
    margin=dict(t=60, b=60),
    **chart_theme
)

# New Members Chart with Updated Colors
new_members_chart = go.Figure()
new_members_chart.add_trace(
    go.Scatter(
        x=["Q1", "Q2", "Q3", "Q4"],
        y=new_members,
        mode="lines+markers",
        marker=dict(size=10, color="#E63946"),  # Red markers
        line=dict(width=3, color="#C4C4C4")  # Gray line
    )
)
new_members_chart.update_layout(
    title="New Members per Quarter 📈",
    xaxis_title="Quarter",
    yaxis_title="New Members",
    height=350,
    margin=dict(t=60, b=80, l=80, r=80),  # Extra padding for better spacing
    **chart_theme
)

# Layout for Reports Page
layout = html.Div(
    [
        # Header
        html.H1("Reports Overview", className="fs-1 text-center mb-4"),

        # Tabs
        dcc.Tabs(
            id="reports-tabs",
            value='tab-1',
            children=[
                dcc.Tab(label='Top Movies', value='tab-1'),
                dcc.Tab(label='Ticket Sales Analysis', value='tab-2'),
                dcc.Tab(label='Statistics & Graphs', value='tab-3'),
            ],
            className="dcc-tabs"
        ),

        # Tab Content
        html.Div(id='reports-tabs-content')
    ]
)

# Callback for Tabs
@dash.callback(
    dash.Output('reports-tabs-content', 'children'),
    [dash.Input('reports-tabs', 'value')]
)
def render_tab_content(tab):
    if tab == 'tab-1':
        return html.Div(
            [
                html.H2("Top Movies", className="section-title"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(
                                    src=movie["link_to_pictures"],
                                    alt=movie["title"],
                                    className="img-fluid"
                                ),
                                html.H4(movie["title"]),
                                html.P(f"⭐ Rating: {movie['ratings']}", className="rating"),
                                html.P(movie["description"], className="text-muted"),
                            ],
                            className="movie-card"
                        )
                        for movie in top_movies
                    ],
                    className="movie-grid"
                ),
            ],
            className="section-wrapper"
        )
    elif tab == 'tab-2':
        return html.Div(
            [
                html.H2("Ticket Sales Analysis", className="section-title"),
                dcc.Graph(figure=ticket_sales_chart)
            ],
            className="section-wrapper"
        )
    elif tab == 'tab-3':
        return html.Div(
            [
                html.H2("Statistics & Graphs", className="section-title"),
                html.Div(
                    [
                        html.H3("Annual Expenses vs. Revenues", className="section-title"),
                        dcc.Graph(figure=expenses_vs_revenues)
                    ]
                ),
                html.Div(
                    [
                        html.H3("New Members per Quarter", className="section-title"),
                        dcc.Graph(figure=new_members_chart)
                    ]
                )
            ],
            className="section-wrapper"
        )
