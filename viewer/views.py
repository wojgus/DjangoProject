from django.shortcuts import render
from django.http import HttpResponse

from viewer.models import Movie

# Create your views here.

def movies(request):
    return render(
        request, template_name='movies.html',
        context={
            'movies': Movie.objects.all()
        }
    )
