import csv
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
# Function to convert storage size to MB
def convert_to_mb(size_str: str):
    if size_str.endswith('MB'):
        return int(size_str[:-2])
    elif size_str.endswith('GB'):
        return int(size_str[:-2]) * 1024
    elif size_str.endswith('TB'):
        return int(size_str[:-2]) * 1024 * 1024
    else:
        return None
    
def output_product_data_to_sql(csv_file_path: str, sql_file_path: str):
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        with open(sql_file_path, mode='w') as sql_file:
            sql_file.write("DELETE FROM Product;\n")
            for row in csv_reader:
                try:
                    rating = float(row['rating']) if row['rating'] and row['rating'].lower() != 'none' else 'NULL'
                    seller_reputation = int(row['seller_reputation']) if row['seller_reputation'] and row['seller_reputation'].lower() != 'none' else 'NULL'
                    brand = f"'{row['brand']}'" if row['brand'] else 'NULL'
                    cpu = f"'{row['cpu']}'" if row['cpu'] else 'NULL'
                    disk = convert_to_mb(row['disk']) if row['disk'] else 'NULL'
                    ram = convert_to_mb(row['ram']) if row['ram'] else 'NULL'
                    post_url = f"'{row['post_url']}'"
                    img_url = f"'{row['img_url']}'"
                    free_shipping = 'TRUE' if row['free_shipping'].lower() == 'true' else 'FALSE'

                    sql_file.write(f'''
                    INSERT INTO Product (title, price, rating, seller_reputation, brand, cpu, disk, ram, post_url, img_url, free_shipping)
                    VALUES ('{row['title']}', {float(row['price'])}, {rating}, {seller_reputation}, {brand}, {cpu}, {disk}, {ram}, {post_url}, {img_url}, {free_shipping});
                    ''')
                except:
                    continue

    print("SQL statements have been written to", sql_file_path)
    
# Function to insert data into the Product table
def insert_product_data(csv_file_path: str):
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cursor = conn.cursor()

    #Warning to delete the products
    confirm = input("This will delete all existing products in the Product table. Do you want to continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        cursor.close()
        conn.close()
        return
    
    # Delete all products
    cursor.execute("DELETE FROM Product")
    conn.commit()
    print("All existing products have been deleted.")

    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            rating = float(row['rating']) if row['rating'] and row['rating'].lower() != 'none' else None
            seller_reputation = int(row['seller_reputation']) if row['seller_reputation'] and row['seller_reputation'].lower() != 'none' else None

            cursor.execute('''
                INSERT INTO Product (title, price, rating, seller_reputation, brand, cpu, disk, ram, post_url, img_url, free_shipping)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                row['title'],
                float(row['price']),
                rating,
                seller_reputation,
                row['brand'] if row['brand'] else None,
                row['cpu'] if row['cpu'] else None,
                convert_to_mb(row['disk']) if row['disk'] else None,
                convert_to_mb(row['ram']) if row['ram'] else None,
                row['post_url'],
                row['img_url'],
                row['free_shipping'].lower() == 'true'
            ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data inserted successfully.")

# Main execution
if __name__ == "__main__":
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mercado_libre_backup.csv') #Change to real csv directory
    sql_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'out.sql') #Change to real csv directory
    # insert_product_data(csv_file_path)
    output_product_data_to_sql(csv_file_path, sql_file_path)