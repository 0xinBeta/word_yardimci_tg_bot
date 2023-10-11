import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

load_dotenv()

# Your Neon database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Parse the database URL
parsed_url = urlparse(DATABASE_URL)

# Connect to the database
conn = psycopg2.connect(
    dbname=parsed_url.path[1:],
    user=parsed_url.username,
    password=parsed_url.password,
    host=parsed_url.hostname,
    port=parsed_url.port
)

# Create a cursor object
cursor = conn.cursor()

# Create the table
create_table_query = '''
CREATE TABLE IF NOT EXISTS words (
    word_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    word_english TEXT NOT NULL,
    word_turkish TEXT NOT NULL,
    word_farsi TEXT NOT NULL,
    example TEXT,
    correct_count INTEGER DEFAULT 0,
    incorrect_count INTEGER DEFAULT 0
);
'''

cursor.execute(create_table_query)

# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
