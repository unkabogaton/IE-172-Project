import dash
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.express as px
from dash.dash_table import Format
from database import fetch_data  # Ensure fetch_data is correct for fetching customer data

# Register the Customers page
dash.register_page(__name__, name="Customers")

# Layout for Customers Page
layout = html.Div([
    html.H1("Customer Information", className="text-center my-4 text-light"),

    # Search Bar
    html.Div([
        dcc.Input(
            id='customer-search-input',
            type='text',
            placeholder='Search customers...',
            debounce=False,
            className='form-control mb-3',
            style={'width': '50%', 'margin': 'auto'}
        )
    ], className='text-center'),

    # Message when no results or empty search
    html.Div(id='no-results-message', className="text-center text-light my-4"),

    # Export Button
    html.Button("Export to Excel", id="export-excel-button", className="btn btn-primary my-4"),
    dcc.Download(id="download-dataframe-xlsx"),

    # Data Table Wrapper
    html.Div(
        id='table-container',  # Wrapper Div for visibility control
        children=[
            dash_table.DataTable(
                id='customers-table',
                columns=[
                    {"name": "Name", "id": "name", "deletable": False},
                    {"name": "Address", "id": "address", "deletable": False},
                    {"name": "Telephone Number", "id": "telephone_number", "deletable": False},
                    {"name": "Email", "id": "email", "deletable": False},
                    {"name": "Ticket Purchase", "id": "ticket_purchase", "deletable": False},
                    {"name": "Ticket Number", "id": "ticket_number", "deletable": False},
                    {"name": "Date", "id": "date", "deletable": False},
                    {"name": "Unit Price", "id": "unit_price", "deletable": False, "type": "numeric"},
                    {"name": "Amount Paid", "id": "amount_paid", "deletable": False, "type": "numeric", "format": Format(precision=2, scheme='fixed')},
                    {"name": "Tickets Purchased", "id": "tickets_purchased", "deletable": False, "type": "numeric"}
                ],
                data=[],  # Will be populated with callback
                sort_action="native",  # Enable sorting on columns
                style_table={'height': '400px', 'overflowY': 'auto'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'color': '#FFF',
                    'backgroundColor': '#222'
                },
                style_header={'backgroundColor': '#333', 'fontWeight': 'bold'},
                page_size=10  # Number of rows per page
            )
        ],
        style={"display": "none"}  # Initially hidden
    ),

    # Customer Details Modal (Initially hidden)
    html.Div([
        dcc.Store(id='selected-customer-data'),
        html.Div(id="customer-modal", style={"display": "none"})
    ]),

    # Insights (Charts)
    html.Div([
        html.H3("Customer Insights", className="text-center my-4 text-light"),
        dcc.Graph(id="top-spending-customers"),
        dcc.Graph(id="ticket-purchase-trends")
    ]),
])


# Callback for Search Filtering
@dash.callback(
    [Output('customers-table', 'data'),
     Output('no-results-message', 'children'),
     Output('table-container', 'style')],
    Input('customer-search-input', 'value'),
    prevent_initial_call=False
)
def update_customer_table(search_value):
    """
    Dynamically filter customers data based on search input.
    """
    if not search_value:
        # No search input: Hide the table and show the default message
        return [], "Search for customers to view their details", {"display": "none"}

    # Fetch filtered data from the database
    try:
        customers_data = fetch_data(
            "customers", 
            conditions=f"name ILIKE '%{search_value}%' OR email ILIKE '%{search_value}%'"
        )
        if not customers_data:
            # No matches found: Hide the table and show the no-results message
            return [], "No customers match your search.", {"display": "none"}
        
        # Convert to DataFrame
        filtered_df = pd.DataFrame(customers_data, columns=["name", "address", "telephone_number", "email", "ticket_purchase", "ticket_number", "date", "unit_price", "amount_paid", "tickets_purchased"])
        return filtered_df.to_dict('records'), "", {"display": "block"}  # Show the table
    except Exception as e:
        print(f"Database error: {e}")
        return [], "An error occurred while fetching data.", {"display": "none"}


# Callback for Exporting Data to Excel
@dash.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("export-excel-button", "n_clicks"),
    prevent_initial_call=True
)
def export_to_excel(n_clicks):
    if n_clicks is None:
        return dash.no_update
    
    # Fetch the data
    customers_data = fetch_data("customers")
    df = pd.DataFrame(customers_data, columns=["name", "address", "telephone_number", "email", "ticket_purchase", "ticket_number", "date", "unit_price", "amount_paid", "tickets_purchased"])
    return dcc.send_data_frame(df.to_excel, "customers.xlsx", index=False)


# Callback for Row Click and Modal View
@dash.callback(
    [Output('selected-customer-data', 'data'),
     Output('customer-modal', 'children')],
    Input('customers-table', 'active_cell')
)
def show_modal_details(active_cell):
    if active_cell:
        row_idx = active_cell['row']
        customer_data = fetch_data("customers")[row_idx]
        modal = html.Div([
            html.H4(f"Details for {customer_data[0]}"),
            html.P(f"Email: {customer_data[3]}"),
            html.P(f"Tickets Purchased: {customer_data[9]}"),
            html.P(f"Amount Paid: ${customer_data[8]:.2f}"),
            html.P(f"Address: {customer_data[1]}"),
            html.P(f"Telephone: {customer_data[2]}"),
            html.P(f"Ticket Purchase: {customer_data[4]}"),
            html.P(f"Ticket Number: {customer_data[5]}"),
            html.P(f"Date: {customer_data[6]}")
        ])
        return customer_data, modal
    return None, None


# Callback for Charts (Top Spending Customers)
@dash.callback(
    Output("top-spending-customers", "figure"),
    Input("customer-search-input", "value")
)
def generate_top_spending_customers_chart(search_value):
    customers_data = fetch_data("customers")
    df = pd.DataFrame(customers_data, columns=["name", "amount_paid"])
    top_customers = df.nlargest(5, "amount_paid")
    fig = px.bar(top_customers, x="name", y="amount_paid", title="Top 5 Spending Customers")
    return fig


# Callback for Ticket Purchase Trends
@dash.callback(
    Output("ticket-purchase-trends", "figure"),
    Input("customer-search-input", "value")
)
def generate_ticket_purchase_trends(search_value):
    customers_data = fetch_data("customers")
    df = pd.DataFrame(customers_data, columns=["date", "tickets_purchased"])
    df['date'] = pd.to_datetime(df['date'])
    df_grouped = df.groupby(df['date'].dt.to_period("M")).sum()
    fig = px.line(df_grouped, x=df_grouped.index.astype(str), y="tickets_purchased", title="Monthly Ticket Purchases")
    return fig
