import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY= os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

# Test hyperparameters
TEMPERATURE_VALUES = [
    0.3,
    0.8,
    1.0,
    1.5,
    2.0
]
TOP_P_VALUES = [
    0.8,
    0.9,
    1.0
]

# Test prompts
TEST_PROMPTS = [
    "Quiero una computadora HP con al menos 8GB de RAM, que tenga suficiente espacio para guardar fotos y videos con mi familia",
    "Computadora para videojuegos de última generación, para jugar a altos FPS y que tenga capacidad para actualizaciones grandes",
    "Una PC para tareas intensas de procesamiento y edición de video, además debe tener buenas reseñas y un vendedor confiable",
    "Quiero una PC para jugar juegos como BD3, Diablo IV, CoD, WoW, Elden Ring, etc. Me gustaría un ordenador que pueda con todo y que dure unos cuantos años. Con precio máximo de 1200$"
]

with open('out.txt', 'a') as f:
    for temperature in TEMPERATURE_VALUES:
        for top_p in TOP_P_VALUES:
            f.write(f"Temperature: {temperature}, Top P: {top_p}\n")
            model = genai.GenerativeModel('gemini-1.5-flash', generation_config={'temperature': temperature, 'top_p': top_p})
            prompt_number = 1
            for prompt in TEST_PROMPTS:
                query = f"""
                    Eres un desarrollador con conocimiento en SQL para bases de datos de Postgres.
                        
                    Escribe una consulta SQL, basada en la petición del usuario, dada la tabla 'Product' con columnas:
                    - id: int
                    - title: varchar, nombre del producto
                    - price: float
                    - rating: float, opcional, de 0 a 5, indica la puntuación promedio dada por clientes
                    - seller_reputation: int, opcional, de 0 a 5. Indica la confiabilidad del vendedor
                    - brand: varchar, opcional, marca de la PC
                    - cpu: varchar, opcional, marca y modelo de CPU
                    - disk: int, opcional, capacidad de almacenamiento en MB
                    - ram: int, opcional, capacidad de RAM en MB
                    - free_shipping: boolean, indica si tiene envío gratis
                    Tu consulta siempre debe seleccionar todos los campos, es decir, SELECT *
                    
                    Responde en formato JSON con dos campos:
                    - data: el SQL si es posible, o un mensaje de error si el usuario hizo una petición incorrecta (como pedir algo que no sea una computadora)
                    - type: 'success' si lograste generar el SQL, 'error' en caso contrario
                    
                    Petición del usuario: {prompt}
                """
                response = model.generate_content(query)
                f.write(f"Response {prompt_number}:\n")
                f.write(response.text)
                f.write("\n")
                prompt_number += 1
            f.write("====\n")
