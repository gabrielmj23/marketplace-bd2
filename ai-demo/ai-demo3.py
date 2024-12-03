import google.generativeai as genai
GOOGLE_API_KEY= 'your-api-key'

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

user_prompt = input("Escriba las especificaciones de la computadora que desea comprar: ")

full_prompt = f"Write a PostgreSQL compatible SQL query, given the table name 'talkermarket' and columns id, title, price, rating, seller_reputation, brand, cpu, disk, ram, post_url, img_url and free_shipping. Note that the disk and ram are measured in MB. {user_prompt}"

response = model.generate_content(full_prompt)
print(response.text)