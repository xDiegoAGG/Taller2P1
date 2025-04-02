from django.shortcuts import render
from movie.models import Movie
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv


# Cargar la API Key
load_dotenv('./api_keys.env')
client = OpenAI(api_key=os.environ.get('openaiApiKey'))

# Función para calcular similitud de coseno
def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Vista de recomendación
def recommendation(request):
    best_movie = None
    max_similarity = -1
    prompt_emb = None

    if request.method == "POST":
        # Obtener el prompt ingresado por el usuario desde el formulario
        prompt = request.POST.get("prompt", "")

        if prompt:
            # Generar embedding del prompt
            response = client.embeddings.create(
                input=[prompt],
                model="text-embedding-3-small"
            )
            prompt_emb = np.array(response.data[0].embedding, dtype=np.float32)

            # Recorrer la base de datos y comparar
            for movie in Movie.objects.all():
                movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
                similarity = cosine_similarity(prompt_emb, movie_emb)

                if similarity > max_similarity:
                    max_similarity = similarity
                    best_movie = movie

    # Renderizar la plantilla con la película recomendada
    return render(request, 'recommendations.html', {
        "best_movie": best_movie,
        "similarity": max_similarity if best_movie else None
    })