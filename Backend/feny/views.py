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
        statement = "SELECT AVG(b.stars) From business b where b.city = %s and b.categories like %s"
        cursor.execute(statement, [city,category])
        row = cursor.fetchone()
        print(row)
    return row

def budget_restaurant(city):
    with connection.cursor() as cursor:
        category = '%Restaurant%'
        statement = "SELECT b.name , b.city From business b, VIKAS.attributes a where b.business_id = a.attr_id and a.pricerange = 1 and b.city = %s and b.categories like %s"
        cursor.execute(statement, [city,category])
        row = cursor.fetchone()
        print(row)
    return row
# def login(request):
# 	return render(request, 'accounts/login.html')