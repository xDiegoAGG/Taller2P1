from django.db import models
import numpy as np

def get_default_array():
    default_arr = np.random.rand(1536)
    return default_arr.tobytes()


class Movie(models.Model):

    title = models.CharField(max_length = 100)
    description = models.CharField(max_length= 280)
    image = models.ImageField(upload_to= 'movie/images/')
    url = models.URLField(blank = True)
    genre = models.CharField(blank = True, max_length= 250)
    year = models.IntegerField(blank = True, null = True)
    emb = models.BinaryField(default=get_default_array())

    def __str__(self):
        return self.title

    def get_embedding(self):
        """Recupera el embedding desde binario como un array de NumPy."""
        return np.frombuffer(self.emb, dtype=np.float32)

    def set_embedding(self, embedding_array):
        """Convierte un array de NumPy a binario y lo almacena en la base de datos."""
        self.emb = np.array(embedding_array, dtype=np.float32).tobytes()
        self.save()