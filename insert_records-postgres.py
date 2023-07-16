import psycopg2

# Establish a connection to the PostgreSQL server
conn = psycopg2.connect(
    host='10.0.4.199',
    port='5432',
    user='postgres',
    password='postgres-pass',
    database='postgres'  # Connect to the default "postgres" database
)

# Set autocommit mode for the connection
conn.autocommit = True

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Check if the database already exists
cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname='students_db'")
database_exists = cursor.fetchone()

# If the database doesn't exist, create it
if not database_exists:
    cursor.execute("CREATE DATABASE students_db")

# Close the cursor and connection
cursor.close()
conn.close()

# Establish a connection to the newly created database
conn = psycopg2.connect(
    host='10.0.4.199',
    port='5432',
    user='postgres',
    password='postgres-pass',
    database='students_db'  # Connect to the "students_db" database
)
cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_query = '''
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        age INTEGER
    )
'''
cursor.execute(create_table_query)

# Generate or prepare the records to insert
records = []
for i in range(15000):
    name = f"Person1{i}"
    age = i + 21
    records.append((name, age))

# Execute the batch insert
sql = "INSERT INTO test_table (name, age) VALUES (%s, %s)"
cursor.executemany(sql, records)

# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
