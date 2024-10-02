from flask import Flask, jsonify, g
import mysql.connector
import time

app = Flask(__name__)

# Function to create and return a new MySQL connection
def connect_to_db():
    retries = 5
    delay = 5
    connection = None
    for i in range(retries):
        try:
            connection = mysql.connector.connect(
                host='mysql-service',  # Matches the service name in docker-compose.yml
                user='root',
                password='password',  # Matches the password in docker-compose.yml
                database='mysql_db',  # Matches the database name in docker-compose.yml
                port=3306
            )
            if connection.is_connected():
                print("Successfully connected to MySQL")
                return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}, retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("Failed to connect to MySQL after multiple retries")

# Function to get a connection (stored in Flask's application context)
def get_db_connection():
    if 'db' not in g:
        g.db = connect_to_db()
    return g.db

# Define route
@app.route('/')
def get_products():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM products')
    results = cursor.fetchall()
    
    if results:
        product_names = ', '.join([product['name'] for product in results])
        return f"flask-service:<br>Products: {product_names}"
    else:
        return 'No products found in the database.', 404

# Close MySQL connection when the app context is torn down
@app.teardown_appcontext
def close_db_connection(exception):
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()
        print("MySQL connection closed.")

# Start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
