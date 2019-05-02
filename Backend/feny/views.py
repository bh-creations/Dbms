from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate
from django.db import connection
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
def index(request):
    if request.method == 'GET':
        info = request.GET
        if('location' in info):
            city = info['location']
            row = sql_category_percentage()
    return render(request, 'feny/index.html')


class BarGraphView(TemplateView):
    template_name = 'feny/bargraph.html'

    def get_context_data(self, **kwargs):
        context = super(BarGraphView, self).get_context_data(**kwargs)
        context['category_percentage'] = self.category_percentage()
        return context

    def category_percentage(self):
        final_data = []
        row = sql_category_percentage()
        row = list(row)

        for tuple in row:
            final_data.append(float(tuple))

        print(type(final_data[0]))
        return final_data


class PieChartView(TemplateView):
    template_name = 'feny/piechart.html'

    def get_context_data(self, **kwargs):
        context = super(PieChartView, self).get_context_data(**kwargs)
        context['labels'], context['popular_city'] = self.popular_city()
        return context

    def popular_city(self):
        popular_city = []
        final_data = []
        labels = []
        row = sql_popular_city()
        for tuple in row:
            labels.append(tuple[0])
            final_data.append(tuple[1])

        popular_city.append(labels)
        popular_city.append(final_data)
        print(popular_city[0])
        return labels, final_data

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

def sql_category_percentage():
    with connection.cursor() as cursor:
        c1 = '%Shopping%'
        c2 = '%Restaurants%'
        c3 = '%Home%'
        c4 = '%Fitness%'
        c5 = '%Arts%'
        c6 = '%Health%'
        c7 = '%Nightlife%'
        c8 = '%Hotel%'
        # Budget Restaurant
        statement = "SELECT 100*Sh/total , 100*Rs/total, 100*Hls/total , 100*Ft/total ,100*Ats/total , 100*Ht/total , 100*Nl/total ,100*htl/total from \
                    (Select Sh, Rs, Hls, Ft, Ats, Ht, Nl ,htl , (Sh + Rs +Hls + Ft + Ats + Ht + Nl + htl) as total \
                    from (select count(*) as Sh from  business natural join rateandreview \
                    where categories like %s), \
                    (select count(*) as Rs from business natural join rateandreview \
                    where categories like %s), \
                    (select count(*) as Hls from  business natural join rateandreview \
                    where categories like %s), \
                    (select count(*) as Ft from  business natural join rateandreview \
                    where categories like %s), \
                    (select count(*) as Ats from business natural join rateandreview \
                    where categories like %s), \
                    (select count(*) as Ht from  business natural join rateandreview \
                    where categories like %s), \
                    (select count(*) as Nl from  business natural join rateandreview \
                    where categories like %s), \
                    (select count(*) as htl from  business natural join rateandreview \
                    where categories like %s))"
        cursor.execute(statement, [c1,c2,c3,c4,c5,c6,c7,c8])
        row = cursor.fetchone()
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

def sql_popular_city():
    with connection.cursor() as cursor:
        # Cheap and Decent hotels to stay at in a particular city
        # statement = "SELECT * From ( SELECT b.city,count(b.business_id) From business b group by b.city order by count(b.business_id) desc) Where rownum = 6"
        statement = "SELECT * From (SELECT b.city,count(b.business_id) From business b group by b.city order by count(b.business_id) desc) where rownum<=6"
        cursor.execute(statement)
        row = cursor.fetchall()
    return row

# def login(request):
# 	return render(request, 'accounts/login.html')