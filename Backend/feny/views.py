from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate

# Create your views here.
from django.http import HttpResponse

def index(request):
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
# def login(request):
# 	return render(request, 'accounts/login.html')