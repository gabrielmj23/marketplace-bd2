from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

pipe = pipeline("text-generation", model="meta-llama/Llama-3.1-8B")

# Function to ask questions
def ask_question(question):
    response = pipe(question, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']

# Example usage
question = "Escribe una consulta en SQL compatible con PostgreSQL, dada la tabla de nombre 'talkermarket' y columnas id, title, price, rating, seller_reputation, brand, cpu, disk, ram, post_url, img_url y free_shipping. La consulta debe hallar todas las computadoras tales que su capacidad de ram sea mayor a 8GB y la reputacion del vendedor sea mayor a 3"
answer = ask_question(question)
print(answer)
