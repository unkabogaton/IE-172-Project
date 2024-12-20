import dash
from dash import html, dcc, Input, Output
import pandas as pd
from database import fetch_data  # Ensure fetch_data works as intended

# Register the Movies page
dash.register_page(__name__, name="Movies")

# Layout for Movies Page
layout = html.Div([
    html.H1("Movie Schedules & Search", className="text-center my-4 text-light"),

    # Search Bar
    html.Div([
        dcc.Input(
            id='search-movie-input',
            type='text',
            placeholder='Search movies...',
            debounce=False,
            className='form-control mb-3',
            style={'width': '50%', 'margin': 'auto'}
        )
    ], className='text-center'),

    # Message when no results are found
    html.Div(id='no-movie-results-message', className="text-center text-light my-4"),

    # Cards Container
    html.Div(
        id='movies-card-container',
        className="d-flex flex-wrap justify-content-center",  # Flexbox for responsive layout
        style={'gap': '20px'}  # Space between cards
    )
])


# Callback for dynamic movie card display
@dash.callback(
    [Output('movies-card-container', 'children'),
     Output('no-movie-results-message', 'children')],
    Input('search-movie-input', 'value'),
    prevent_initial_call=False
)
def update_movies(search_value):
    """
    Dynamically display movie cards. 
    - Default: Show all cards from scheduling table.
    - On Search Input: Show filtered cards from movies table.
    """
    try:
        if search_value:
            # Fetch filtered movies from the 'movies' table
            condition = f"title ILIKE '%{search_value}%'"
            movie_data = fetch_data("movies", conditions=condition)

            if not movie_data:
                # No results found
                return [], "No movies match your search."

            # Convert to DataFrame
            movies_df = pd.DataFrame(movie_data, columns=["link_to_pictures", "title", "ratings", "description"])

            # Generate Cards for 'movies' table
            cards = [
                html.Div([
                    # Movie Image
                    html.Img(src=movie['link_to_pictures'], className="card-img-top", 
                             style={"height": "300px", "objectFit": "cover"}),

                    # Card Body
                    html.Div([
                        # Movie Title and Ratings
                        html.H5(movie['title'], className="card-title", 
                                style={"color": "white", "textAlign": "center"}),

                        html.P(f"Ratings: {movie['ratings']}", className="card-text", 
                               style={"color": "yellow", "fontSize": "16px", "textAlign": "center"}),

                        # Movie Description
                        html.P(movie['description'], className="card-text",
                               style={"color": "white", "fontSize": "12px", "textAlign": "center"})
                    ], className="card-body", style={"backgroundColor": "#333"})
                ],
                className="card",
                style={"width": "18rem", "border": "1px solid #444", "boxShadow": "0px 4px 8px rgba(0,0,0,0.3)"}
                )
                for movie in movies_df.to_dict('records')
            ]
            return cards, ""  # Display filtered cards and clear the message

        else:
            # Default View: Fetch all data from 'scheduling' table
            scheduling_data = fetch_data("scheduling")

            if not scheduling_data:
                return [], "No movie schedules available."

            # Convert to DataFrame
            schedules_df = pd.DataFrame(scheduling_data, columns=["link_to_pictures", "movie_title", "showtimes", "duration", "capacity"])

            # Generate Cards for 'scheduling' table
            cards = [
                html.Div([
                    # Movie Image
                    html.Img(src=schedule['link_to_pictures'], className="card-img-top", 
                             style={"height": "300px", "objectFit": "cover"}),

                    # Card Body
                    html.Div([
                        # Movie Title
                        html.H5(schedule['movie_title'], className="card-title", 
                                style={"color": "white", "textAlign": "center"}),

                        # Movie Details
                        html.P(
                            f"Showtimes: {schedule['showtimes']} | Duration: {schedule['duration']} mins | Capacity: {schedule['capacity']}",
                            className="card-text",
                            style={"color": "yellow", "fontSize": "14px", "textAlign": "center"}
                        )
                    ], className="card-body", style={"backgroundColor": "#333"})
                ],
                className="card",
                style={"width": "18rem", "border": "1px solid #444", "boxShadow": "0px 4px 8px rgba(0,0,0,0.3)"}
                )
                for schedule in schedules_df.to_dict('records')
            ]
            return cards, ""  # Display all cards from scheduling table

    except Exception as e:
        print(f"Database error: {e}")
        return [], "An error occurred while fetching movie data."
