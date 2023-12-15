import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(database="test", user="postgres", password="pierro", host="localhost", port="5432")

# Create a cursor object to interact with the database
cur = conn.cursor()

# IF table already exists, drop it
cur.execute("DROP TABLE IF EXISTS users")

# Create the table "users" with the column "id"
cur.execute("CREATE TABLE users (id INT)")

# Insert a new row with id=0
cur.execute("INSERT INTO users (id) VALUES (-1)")

# Commit the changes to the database
conn.commit()

# Close the cursor and the database connection
cur.close()
conn.close()