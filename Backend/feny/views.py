from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate
from django.db import connection
from django.http import HttpResponse

# Create your views here.
def index(request):
    if request.method == 'GET':
        info = request.GET
        if('location' in info):
            city = info['location']
            row = average_rating(city)
    return render(request, 'feny/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
        	user = form.save()
        	username = form.cleaned_data.get('username')
        	raw_password = form.cleaned_data.get('password1')
        	# user = authenticate(username=username, password=raw_password)
        	login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        	return redirect('/feny/')
    else:
    	form = UserCreationForm()
    return render(request, 'feny/signup.html', {'form': form})

def average_rating(city):
    with connection.cursor() as cursor:
        category = '%Restaurant%'
        # Finding average restaurant rating of each city
        statement = "SELECT AVG(b.stars) From business b where b.city = %s and b.categories like %s"
        cursor.execute(statement, [city,category])
        row = cursor.fetchone()
        print(row)
    return row

def budget_restaurant(city):
    with connection.cursor() as cursor:
        category = '%Restaurant%'
        # Budget Restaurant
        statement = "SELECT b.name , b.city From business b, attributes a where b.business_id = a.attr_id and a.pricerange = 1 and b.city = %s and b.categories like %s"
        cursor.execute(statement, [city,category])
        row = cursor.fetchone()
        print(row)
    return row

def search_by_cuisine(cuisine):
    with connection.cursor() as cursor:
        category = '%Restaurant%'
        # Search restaurants according to Cuisine
        statement = "SELECT b.name From business b where b.categories like %s and b.categories like %s"
        cursor.execute(statement, [category,cuisine])
        row = cursor.fetchone()
        print(row)
    return row

def deliver_restaurant():
    with connection.cursor() as cursor:
        category = '%Restaurant%'
        # Total number of restaurants that make deliveries in each city
        statement = "SELECT b.city, count(*) From business b, attributes a where B.business_id = a.attr_id and  b.categories like %s and a.delivery = 1 Group by b.city"
        cursor.execute(statement, [category])
        row = cursor.fetchone()
        print(row)
    return row

def best_pizza(city):
    with connection.cursor() as cursor:
        category = '%Pizza%'
        # Best Pizza places to eat in a particular city(stars >=3)
        statement = "SELECT b.name From business B where b.categories like %s and b.stars >= 3 and b.city = %s"
        cursor.execute(statement, [category,city])
        row = cursor.fetchone()
        print(row)
    return row    

def food_alcohol(city):
    with connection.cursor() as cursor:
        c1 = '%Restaurants%'
        c2 = '%Wine%'
        c3 = '%Spirits%'
        c4 = '%Beer%'
        c5 = '%Pubs%'
        c6 = '%Bars%'
        # Places that serve food as well as alcohol in a particular city
        statement = "SELECT b.name From business B where b.city = %s and  b.categories like %s and (b.categories like %s or b.categories like %s or b.categories like %s or b.categories = %s or b.categories = %s)"
        cursor.execute(statement, [city,c1,c2,c3,c4,c5,c6])
        row = cursor.fetchone()
        print(row)
    return row  

def cheap_hotel(city):
    with connection.cursor() as cursor:
        category = '%Hotels%'
        # Cheap and Decent hotels to stay at in a particular city
        statement = "SELECT b.name From business B, attributes a where b.business_id = a.attr_id and b.city = %s and b.categories like %s and b.stars >=3 and a.pricerange <= 3"
        cursor.execute(statement, [city,category])
        row = cursor.fetchone()
        print(row)
    return row 
# def login(request):
# 	return render(request, 'accounts/login.html')