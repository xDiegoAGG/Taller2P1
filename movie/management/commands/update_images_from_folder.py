import os
import re
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update images :D"

    def handle(self, *args, **kwargs):
        updated_count = 0

        for movie in Movie.objects.all():
            clean_title = self.remove_special_characters(movie.title)
            image_path = f"./media/movie/images/m_{clean_title}.png"
            
            if not os.path.exists(image_path):
                self.stderr.write(f"Image file 'm_{clean_title}.png' not found.")
            else:
                movie.image = f"movie/images/m_{clean_title}.png"
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title} image successfully loaded"))

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies image from Images Folder."))

    def remove_special_characters(self, text):
        return re.sub(r'[^a-zA-Z0-9_\- ]', '', text)  # Elimina caracteres especiales excepto guiones y espacios
