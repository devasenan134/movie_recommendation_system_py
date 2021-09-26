from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Movie, Genre, Rating
from django.db import connection
from collections import namedtuple



def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def home(request):
    cursor = connection.cursor()
    recent = Movie.objects.raw("select * from mrs_movie order by year desc, mth limit 6") 
    popular = Movie.objects.raw("select * from mrs_movie order by avg_rate desc limit 6")
    based_rating = []
    # popular_genres = set()
    # for i in popular:
    #     popular_genres.add(i.genres.all())
    # print(popular_genres)
    
    if request.user.is_authenticated:
        fav_genres = set()
        fav_movies = set()
        rated_movies = Movie.objects.raw(f"select * from mrs_movie m where id in (select movie_id from mrs_rating r where r.user_id ={request.user.id})")
        for i in Movie.objects.raw(f"select * from mrs_movie m where id in (select movie_id from mrs_rating r where r.user_id ={request.user.id} and r.rate>=3)"):
            fav_movies.add(i)
        for j in fav_movies:
            for k in j.genres.all():
                fav_genres.add(k.id)
        fav_genres = tuple(fav_genres)
        for i in fav_genres:
            movies_in_genre = Genre.objects.get(id=i)
            based_rating.extend(movies_in_genre.has_movies.all())
        based_rating = set(based_rating).difference(rated_movies)
        if len(based_rating) == 0:
            based_rating = None
        print(based_rating)
        print(fav_movies)
        return render(request, 'mrs/home.html', {
            "recent": recent,
            "popular": popular,
            "based_ratings": based_rating
            })
    else:
        
        return render(request, 'mrs/home.html', {
            "recent": recent,
            "popular": popular,
            })


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
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    tot_rate = 0
    movie.no_votes = len(Rating.objects.raw(f"select * from mrs_rating where movie_id={movie.id}"))
    for i in  Rating.objects.raw(f"select * from mrs_rating where movie_id={movie.id}"):
        tot_rate += i.rate
    try:
        movie.avg_rate = tot_rate/movie.no_votes
    except:
        movie.avg_rate = 0
    movie.save()
        
    try:
        rating = Rating.objects.get(movie = movie, user = request.user)
        rate = rating.rate
    except:
        rate = None
    print(rate)
    if request.method == 'GET':
        return render(request, 'mrs/watch_movie.html', {
            "movie": movie,
            "rating": rate,
            "month": months[movie.mth-1],
        })
    else:
        if request.user.is_authenticated:
            rate = request.POST.get('rate')
            rating = Rating(movie = movie, user = request.user, rate = rate)
            rating.save()
            
            tot = 0
            movie.no_votes = len(Rating.objects.raw(f"select * from mrs_rating where movie_id={movie.id}"))
            for i in  Rating.objects.raw(f"select * from mrs_rating where movie_id={movie.id}"):
                tot += i.rate
            movie.avg_rate = tot_rate/movie.no_votes
            movie.save()
            print(rate, rating.user.id)
            return redirect("home")
        else:
            return render(request, 'mrs/watch_movie.html', {
                "movie": movie,
                "rating": rate,
                "month": months[movie.mth-1],
                "error": "Login Required!"
            })
