import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
load_dotenv()
# Function to create the database if it doesn't exist
def create_database():
    conn = psycopg2.connect(
        dbname= 'postgres',
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Check if the database exists
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'talkermarket'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE talkermarket"))
        print("Database 'talkermarket' created successfully.")
    else:
        print("Database 'talkermarket' already exists.")

    cursor.close()
    conn.close()

# Function to create the Product table
def create_product_table():
    conn = psycopg2.connect(
        dbname='talkermarket',
        user='postgres',
        password='admin',
        host='localhost',
        port='5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Product (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        price FLOAT NOT NULL,
        rating FLOAT CHECK (rating >= 0 AND rating <= 5) DEFAULT NULL,
        seller_reputation INT CHECK (seller_reputation >= 0 AND seller_reputation <= 5) DEFAULT NULL,
        brand VARCHAR(30) DEFAULT NULL,
        cpu VARCHAR(30) DEFAULT NULL,
        disk INT CHECK (disk > 0) DEFAULT NULL,
        ram INT CHECK (ram > 0) DEFAULT NULL,
        post_url TEXT,
        img_url TEXT,
        free_shipping BOOLEAN
    )
    '''
    cursor.execute(create_table_query)
    print("Table 'Product' created successfully.")

    cursor.close()
    conn.close()

# Main execution
if __name__ == "__main__":
    create_database()
    create_product_table()