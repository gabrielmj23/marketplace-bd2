import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY= os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

user_prompt = input("Escriba las especificaciones de la computadora que desea comprar: ")

full_prompt = f"Write a PostgreSQL compatible SQL query, given the table name 'Product' and columns id, title, price, rating, seller_reputation, brand, cpu, disk, ram, post_url, img_url and free_shipping. Note that the disk and ram are measured in MB. Make sure to responde with the SQL query and only the SQL query, no additional context or explanation is needed. {user_prompt}"

response = model.generate_content(full_prompt)
print(response.text)
