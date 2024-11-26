import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}
payload = {
    "inputs": "Write a PostgreSQL compatible SQL query, given the table name 'talkermarket' and columns id, title, price, rating, seller_reputation, brand, cpu, disk, ram, post_url, img_url and free_shipping. The query should find all computers such that their ram capacity is greater than 8000MB and the seller reputation is greater than 3.",
}

response = requests.post(API_URL, headers=headers, json=payload)
print(response.json())
