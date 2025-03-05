import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie
def statistics_view(request):
    matplotlib.use('Agg')
    all_movies = Movie.objects.all()

    # Crear un diccionario para almacenar la cantidad de películas por año
    movies_counts_by_year = {}
    movies_counts_by_genre = {}
    # Contar la cantidad de películas por año
    for movie in all_movies:
        year = movie.year if movie.year else 'None'
        genre = movie.genre.split(',')[0] if movie.genre else 'None'

        if year in movies_counts_by_year:
            movies_counts_by_year[year] += 1
        else:
            movies_counts_by_year[year] = 1

        if genre in movies_counts_by_genre:
            movies_counts_by_genre[genre] += 1
        else:
            movies_counts_by_genre[genre] = 1

    # Configurar las posiciones y anchos de las barras
    bar_width = 0.5
    bar_positions = range(len(movies_counts_by_year))
    bar_positions2 = range(len(movies_counts_by_genre))
    # Crear la gráfica de barras
    plt.bar(bar_positions, movies_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Movie number')
    plt.xticks(bar_positions, movies_counts_by_year.keys(), rotation=90)

    # Ajustar el espacio en la parte inferior
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.clf()
    
    # Convertir la imagen a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    # Crear la gráfica de barras
    plt.bar(bar_positions2, movies_counts_by_genre.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Movie number')
    plt.xticks(bar_positions2, movies_counts_by_genre.keys(), rotation=90)

    # Ajustar el espacio en la parte inferior
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.clf()

    image_png = buffer.getvalue()
    buffer.close()
    graphic2 = base64.b64encode(image_png).decode('utf-8')


    # Renderizar la plantilla con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic, 'graphic2':graphic2})



# Create your views here.


def home(request): 
    #return HttpResponse('<h1>Hello motherfleckers</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': 'María Acevedo Suárez'})
    searchTerm =   request.GET.get('searchMovie') 
    if searchTerm:
        movies = Movie.objects.filter(title__icontains = searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm' : searchTerm , 'movies' : movies})

def about(request):
    return render(request, 'about.html')
def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})