from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate
from django.db import connection
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.urls import resolve
import json

# Create your views here.
def index(request):
    if request.method == 'GET':
        info = request.GET
        if('location' in info):
            city = info['location']
            row = sql_month_review_star()
    return render(request, 'feny/index.html')


class Bar_Category_Percentage(TemplateView):
    template_name = 'feny/bargraph.html'

    def get_context_data(self, **kwargs):
        context = super(Bar_Category_Percentage, self).get_context_data(**kwargs)
        context['labels'], context['data'], context['title'] = self.category_percentage()
        return context

    def category_percentage(self):
        final_data = []
        row = sql_category_percentage()
        row = list(row)
        labels = ['Shopping', 'Restaurants', 'Home', 'Fitness', 'Arts', 'Health', 'Nightlife', 'Hotel']
        title = ['Category Percentage']
        for tuple in row:
            final_data.append(float(tuple))

        # print(type(final_data[0]))
        return labels, final_data, title


class Pie_Popular_City(TemplateView):
    template_name = 'feny/piechart.html'
    def get_context_data(self, **kwargs):
        context = super(Pie_Popular_City, self).get_context_data(**kwargs)
        context['labels'], context['data'], context['title'] = self.popular_city()
        return context

    def popular_city(self):
        final_data = []
        labels = []
        row = sql_popular_city()
        title = ['Cities with most business']
        for tuple in row:
            labels.append(tuple[0])
            final_data.append(tuple[1])

        # print(popular_city[0])
        return labels, final_data, title

class Pie_Review_Distribution(TemplateView):
    template_name = 'feny/piechart.html'
    def get_context_data(self, **kwargs):
        context = super(Pie_Review_Distribution, self).get_context_data(**kwargs)
        context['labels'], context['data'], context['title'] = self.review_distribution()
        return context

    def review_distribution(self):

        final_data = []
        labels = ['1 star', '2 star', '3 star', '4 star', '5 star']
        title = ['Review Distribution']
        row = sql_review_distribution()
        for tuple in row:
            final_data.append(float(tuple))


        # print(popular_city[0])
        return labels, final_data, title

class Line_Month_Review_Star(TemplateView):
    template_name = 'feny/linechart.html'
    def get_context_data(self, **kwargs):
        context = super(Line_Month_Review_Star, self).get_context_data(**kwargs)
        context['data_1'],context['data_2'],context['data_3'],context['data_4'],context['data_5'], context['title'] = self.month_review_star()
        return context

    def month_review_star(self):
        final_data = [[],[],[],[],[]]

        title = ['# of reviews by Month, by # of Stars']
        row = sql_month_review_star()
        for tuple in row:
            if tuple[5] is not None and tuple[6] is not None:
                for i in range(5):
                    point = {}
                    if tuple[5] < 10:
                        date = str(tuple[6]) + '-0' + str(tuple[5])
                    else:
                        date = str(tuple[6]) + '-' + str(tuple[5])
                    point['x'] = date
                    point['y'] = tuple[i]
                    final_data[i].append(point)
        
        # print(json.dumps(final_data[0]))
        # print(popular_city[0])
        return final_data[0],final_data[1],final_data[2],final_data[3],final_data[4],title



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
        # print(row)
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

def sql_review_distribution():
    with connection.cursor() as cursor:

        statement = "SELECT 100*onestar/total, 100*twostar/total , 100*threestar/total, 100*fourstar/total , 100*fivestar/total from \
                    (SELECT onestar, twostar, threestar, fourstar, fivestar , (onestar+ twostar+ threestar+ fourstar+ fivestar) as total from \
                    (SELECT count(*) as onestar from reviewdates , rateandreview where reviewdates.r_id = rateandreview.r_id and rateandreview.rating = 1), \
                    (SELect count(*) as twostar from reviewdates , rateandreview where reviewdates.r_id = rateandreview.r_id and rateandreview.rating = 2), \
                    (SELect count(*) as threestar from reviewdates , rateandreview where reviewdates.r_id = rateandreview.r_id and rateandreview.rating = 3), \
                    (SELect count(*) as fourstar from reviewdates , rateandreview where reviewdates.r_id = rateandreview.r_id and rateandreview.rating = 4), \
                    (SELect count(*) as fivestar from reviewdates , rateandreview where reviewdates.r_id = rateandreview.r_id and rateandreview.rating = 5))"
        cursor.execute(statement)
        row = cursor.fetchone()
        # print(row)
    return row

def sql_month_review_star():
    with connection.cursor() as cursor:
        # Budget Restaurant
        statement = "SELECT nvl(onecount,0) , nvl(twocount,0) , nvl(threecount,0), nvl(fourcount,0) ,nvl(fivecount,0), mon1 , yy1 from \
                    (((((SELECT count(*) as twocount , extract(month from reviewdates.review_date) as mon2, extract(year from reviewdates.review_date) as yy2 \
                    from reviewdates , rateandreview where reviewdates.r_id = rateandreview.r_id and rateandreview.rating = 2 \
                    group by extract(year from reviewdates.review_date), extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) full outer join (SELECT count(*) as onecount , \
                    extract(month from reviewdates.review_date) as mon1, extract(year from reviewdates.review_date) as yy1 \
                    from reviewdates , rateandreview where reviewdates.r_id = rateandreview.r_id and rateandreview.rating = 1 \
                    group by extract(year from reviewdates.review_date), extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) on mon1=mon2 and yy2=yy1)full outer join \
                    (SELECT count(*) as threecount , extract(month from reviewdates.review_date) as mon3, \
                    extract(year from reviewdates.review_date) as yy3 from reviewdates , rateandreview where reviewdates.r_id = rateandreview.r_id \
                    and rateandreview.rating = 3 group by extract(year from reviewdates.review_date), extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) on mon1 = mon3 and yy1 = yy3) full outer join \
                    (SELECT count(*) as fourcount , extract(month from reviewdates.review_date) as mon4, extract(year from reviewdates.review_date) as yy4 \
                    from reviewdates , rateandreview where reviewdates.r_id = rateandreview.r_id and rateandreview.rating = 4 \
                    group by extract(year from reviewdates.review_date), extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) on mon1= mon4 and yy1 = yy4) full outer join \
                    (SELECT count(*) as fivecount , extract(month from reviewdates.review_date) as mon5, \
                    extract(year from reviewdates.review_date) as yy5 from reviewdates , rateandreview \
                    where reviewdates.r_id = rateandreview.r_id and rateandreview.rating = 5 \
                    group by extract(year from reviewdates.review_date), extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) on mon1 = mon5 and yy1 = yy5)"
        cursor.execute(statement)
        row = cursor.fetchall()

    return row

def budget_restaurant(city):
    with connection.cursor() as cursor:
        category = '%Restaurant%'
        # Budget Restaurant
        statement = "SELECT b.name , b.city From business b, attributes a where b.business_id = a.attr_id and a.pricerange = 1 and b.city = %s and b.categories like %s"
        cursor.execute(statement, [city,category])
        row = cursor.fetchone()
        # print(row)
    return row

def search_by_cuisine(cuisine):
    with connection.cursor() as cursor:
        category = '%Restaurant%'
        # Search restaurants according to Cuisine
        statement = "SELECT b.name From business b where b.categories like %s and b.categories like %s"
        cursor.execute(statement, [category,cuisine])
        row = cursor.fetchone()
        # print(row)
    return row

def deliver_restaurant():
    with connection.cursor() as cursor:
        category = '%Restaurant%'
        # Total number of restaurants that make deliveries in each city
        statement = "SELECT b.city, count(*) From business b, attributes a where B.business_id = a.attr_id and  b.categories like %s and a.delivery = 1 Group by b.city"
        cursor.execute(statement, [category])
        row = cursor.fetchone()
        # print(row)
    return row

def best_pizza(city):
    with connection.cursor() as cursor:
        category = '%Pizza%'
        # Best Pizza places to eat in a particular city(stars >=3)
        statement = "SELECT b.name From business B where b.categories like %s and b.stars >= 3 and b.city = %s"
        cursor.execute(statement, [category,city])
        row = cursor.fetchone()
        # print(row)
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
        # print(row)
    return row  

def cheap_hotel(city):
    with connection.cursor() as cursor:
        category = '%Hotels%'
        # Cheap and Decent hotels to stay at in a particular city
        statement = "SELECT b.name From business B, attributes a where b.business_id = a.attr_id and b.city = %s and b.categories like %s and b.stars >=3 and a.pricerange <= 3"
        cursor.execute(statement, [city,category])
        row = cursor.fetchone()
        # print(row)
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