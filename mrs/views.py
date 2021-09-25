from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Movie, Genre, Rating

def home(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    return render(request, 'mrs/home.html', {
        "movies": movies,
        "genres": genres})

@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    
def signupuser(request) :
    if request.method == 'GET':    
        return render(request, 'mrs/signupuser.html', {
            'form': UserCreationForm()
        })
    else :
        if request.POST['password1'] == request.POST['password2'] :
            try :
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError :
                return render(request, 'mrs/signupuser.html', {
                    'error': 'That Username already exists'
                })

        else :
            return render(request, 'mrs/signupuser.html', {
                'form': UserCreationForm(), 'error': 'Passwords did not match'
            })

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'mrs/loginuser.html')
    else:
        if request.POST['username'] == '' or request.POST['password'] == '':
            return render(request, 'mrs/loginuser.html', {
                'error': 'Fill the details'
            })
        else:
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            if user is None:
                return render(request, 'mrs/loginuser.html', {
                    'error': 'Username and password did not match'
                })
            else:
                login(request, user)
                return redirect('home')  
            
def watch_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rate = None
    try:
        rating = Rating.objects.get(movie_id = movie_pk, user_id = request.user)
        rate = rating.rate
    except:
        rate = None
        
    if request.method == 'GET':
        return render(request, 'mrs/watch_movie.html', {
            "movie": movie,
            "rating": rate
        })
    else:
        if request.user.is_authenticated:
            rate = request.POST.get('rate')
            rating = Rating(movie_id = movie, user_id = request.user, rate = rate)
            rating.save()
            
            tot = movie.avg_rate*movie.no_votes
            movie.no_votes += 1
            movie.avg_rate = (tot + int(rate))//movie.no_votes
            movie.save()
            
            return render(request, 'mrs/watch_movie.html', {
                "movie": movie,
                "rating": rate
            })
        else:
            return render(request, 'mrs/watch_movie.html', {
                "movie": movie,
                "rating": rate,
                "error": "Login Required!"
            })
            
def suggestions():
    pass