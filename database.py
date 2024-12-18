import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection parameters
db_config = {
    'dbname': 'project_ni_mhon',
    'user': 'user',
    'password': 'mypassword',
    'host': 'localhost',
    'port': '5432'
}

def fetch_data(table_name, columns="*", conditions=None, order_column="year", order_direction="ASC", limit=None):
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Create the query dynamically
        query = f"SELECT {columns} FROM {table_name}"
        
        # Add conditions to the query if provided
        if conditions:
            query += f" WHERE {conditions}"
        
        # Add the order by clause
        query += f" ORDER BY {order_column} {order_direction}"
        
        # Add limit if provided
        if limit:
            query += f" LIMIT {limit}"

        # Execute the query
        cursor.execute(query)
        results = cursor.fetchall()

        # Return results as a list of dictionaries
        return results
    except Exception as e:
        print(f"Database error: {e}")
        return []
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
