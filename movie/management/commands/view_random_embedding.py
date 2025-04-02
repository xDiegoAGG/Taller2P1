import os
import numpy as np
import random
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Display the embeddings of a randomly selected movie."

    def handle(self, *args, **kwargs):
        # ✅ Fetch all movies from the database
        movies = Movie.objects.all()
        if not movies:
            self.stdout.write(self.style.WARNING("⚠ No movies found in the database."))
            return

        # ✅ Select a random movie
        movie = random.choice(movies)
        embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)
        
        # ✅ Display movie title and first few values of embedding
        self.stdout.write(self.style.SUCCESS(f"🎬 Selected movie: {movie.title}"))
        self.stdout.write(f"Embedding (first 5 values): {embedding_vector[:5]}")