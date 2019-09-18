import threading

from django.shortcuts import render

from .models import Person, Film


# Create your views here.
def index(request):
    f = Film.objects.order_by('-date_updated').first()
    if not f or f.time_to_update():
        print('Time to update')

        data = Film.retrieve_data('films')
        Film.insert_data(data=data)

        data = Person.retrieve_data('people')
        # Execute in a separate thread because it is an IO-bound task which takes long time to execute
        t = threading.Thread(target=Person.insert_data, args=(data, ))
        t.start()

    films = Film.objects.all()

    return render(request, 'movie_list/movies.html', context={'films': films})
