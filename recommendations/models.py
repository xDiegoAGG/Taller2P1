from django.db import models



class Recommendation(models.Model):

    title = models.CharField(max_length = 100)
    description = models.CharField(max_length= 280)
    image = models.ImageField(upload_to= 'movie/images/')
    prompt = models.CharField(max_length = 280)

    def __str__(self):
        return self.title