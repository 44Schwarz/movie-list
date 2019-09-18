from django.shortcuts import render

from .models import Person, Film


# Create your views here.
def index(request):
    f = Film.objects.first()
    if f and f.time_to_update():
        print('Time to update')
        data = Film.retrieve_data('films')
        Film.insert_data(data=data)
    films = Film.objects.all()
    return render(request, 'movie_list/movies.html', context={'films': films})
