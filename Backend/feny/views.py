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
        if 'location' in info and 'business' in info:
            city = info['location']
            bname = info['business']
            row = sql_average_monthly_rating()
            # row = search_by_business_city(bname,city)
            print(row)
        elif 'location' in info:
            city = info['location']
            row = search_by_city(city)

            print(row)
        elif 'business' in info:
            bname = info['business']
            row = search_by_business(bname)
            
            print(row)

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

        return labels, final_data, title

class Line_Month_Review_Star(TemplateView):
    template_name = 'feny/linechart.html'
    def get_context_data(self, **kwargs):
        context = super(Line_Month_Review_Star, self).get_context_data(**kwargs)
        context['data_1'],context['data_2'],context['data_3'],context['data_4'],context['data_5'], context['title'], context['display_format'] = self.month_review_star()
        return context

    def month_review_star(self):
        final_data = [[],[],[],[],[]]

        title = ['Number of reviews by Month, by number of Stars']
        display_format = ['YYYY']
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
        return final_data[0],final_data[1],final_data[2],final_data[3],final_data[4],title,display_format


class Line_Business_Open(TemplateView):
    template_name = 'feny/linechart2.html'
    def get_context_data(self, **kwargs):
        context = super(Line_Business_Open, self).get_context_data(**kwargs)
        context['data_1'],context['data_2'],context['data_3'],context['data_4'],context['data_5'], context['labels'], context['title'],context['display_format'] = self.business_open()
        return context

    def business_open(self):
        final_data = {}
        labels = []
        display_format = ['YYYY']
        title = ['Number of newly opened business in top 5 popular city by month']
        row = sql_business_open()
        for tuple in row:
            if tuple[0] is not None and tuple[1] is not None and tuple[2] is not None and tuple[3] is not None:
                point = {}
                if tuple[3] < 10:
                    date = str(tuple[2]) + '-0' + str(tuple[3])
                else:
                    date = str(tuple[2]) + '-' + str(tuple[3])
                point['x'] = date
                point['y'] = tuple[1]
                if tuple[0] in final_data:
                    final_data[tuple[0]].append(point)
                else:
                    labels.append(tuple[0])
                    final_data[tuple[0]] = [point]
        
        # print(json.dumps(final_data[0]))
        # print(popular_city[0])
        return final_data[labels[0]],final_data[labels[1]],final_data[labels[2]],final_data[labels[3]],final_data[labels[4]],labels,title,display_format

class Line_Business_Close(TemplateView):
    template_name = 'feny/linechart3.html'
    def get_context_data(self, **kwargs):
        context = super(Line_Business_Close, self).get_context_data(**kwargs)
        context['data_1'],context['data_2'],context['data_3'],context['data_4'],context['data_5'], context['labels'], context['title'],context['display_format'] = self.business_close()
        return context

    def business_close(self):
        final_data = {}
        labels = []
        display_format = ['YYYY']
        title = ['Number of closed business in top 5 popular city by month']
        row = sql_business_close()
        for tuple in row:
            if tuple[0] is not None and tuple[1] is not None and tuple[2] is not None and tuple[3] is not None:
                point = {}
                if tuple[3] < 10:
                    date = str(tuple[2]) + '-0' + str(tuple[3])
                else:
                    date = str(tuple[2]) + '-' + str(tuple[3])
                point['x'] = date
                point['y'] = tuple[1]
                if tuple[0] in final_data:
                    final_data[tuple[0]].append(point)
                else:
                    labels.append(tuple[0])
                    final_data[tuple[0]] = [point]
        
        # print(json.dumps(final_data[0]))
        # print(popular_city[0])
        return json.dumps(final_data[labels[0]]),json.dumps(final_data[labels[1]]),json.dumps(final_data[labels[2]]),json.dumps(final_data[labels[3]]),json.dumps(final_data[labels[4]]),labels,title,display_format

class Average_Monthly_Rating(TemplateView):
    template_name = 'feny/linechart4.html'
    def get_context_data(self, **kwargs):
        context = super(Average_Monthly_Rating, self).get_context_data(**kwargs)
        context['data'],context['labels'], context['title'],context['display_format'] = self.average_monthly_rating()
        return context

    def average_monthly_rating(self):
        final_data = [[],[],[],[],[],[]]
        labels = ['Resatuarant','Shopping','Home','Fitness','Arts','Health']
        display_format = ['YYYY']
        title = ['Average rating of categories by month']
        row = sql_average_monthly_rating()
        for tuple in row:
            if tuple[6] is not None and tuple[7] is not None:
                for i in range(6):
                    point = {}
                    if tuple[6] < 10:
                        date = str(tuple[7]) + '-0' + str(tuple[6])
                    else:
                        date = str(tuple[7]) + '-' + str(tuple[6])
                    point['x'] = date
                    point['y'] = float(tuple[i])
                    final_data[i].append(point)
        
        # print(json.dumps(final_data[0]))
        # print(popular_city[0])
        return final_data,labels,title,display_format

class Average_Monthly_Rating_Cuisine(TemplateView):
    template_name = 'feny/linechart5.html'
    def get_context_data(self, **kwargs):
        context = super(Average_Monthly_Rating_Cuisine, self).get_context_data(**kwargs)
        context['data'],context['labels'], context['title'],context['display_format'] = self.average_monthly_rating_cuisine()
        return context

    def average_monthly_rating_cuisine(self):
        final_data = [[],[],[],[],[],[]]
        labels = ['American','Chinese','Japanese','Italian','Mexican','Thai']
        display_format = ['YYYY']
        title = ['Average rating of cuisine by month']
        row = sql_average_monthly_rating_cuisine()
        for tuple in row:
            if tuple[6] is not None and tuple[7] is not None:
                for i in range(6):
                    point = {}
                    if tuple[6] < 10:
                        date = str(tuple[7]) + '-0' + str(tuple[6])
                    else:
                        date = str(tuple[7]) + '-' + str(tuple[6])
                    point['x'] = date
                    point['y'] = float(tuple[i])
                    final_data[i].append(point)
        
        # print(json.dumps(final_data[0]))
        # print(popular_city[0])
        return final_data,labels,title,display_format

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

    return row

def search_by_city(city):
    with connection.cursor() as cursor:
        # category = '%Restaurant%'
        # Search restaurants according to Cuisine
        statement = "SELECT b.name From business b where b.city = %s"
        cursor.execute(statement, [city])
        row = cursor.fetchall()
    return row

def search_by_business(bname):
    with connection.cursor() as cursor:
        name = '%' + bname + '%'
        # Search restaurants according to Cuisine
        statement = "SELECT b.name From business b where b.name like %s"
        cursor.execute(statement, [name])
        row = cursor.fetchall()
    return row

def search_by_business_city(bname,city):
    with connection.cursor() as cursor:
        name = '%' + bname + '%'
        # Search restaurants according to Cuisine
        statement = "SELECT b.name From business b where b.name like %s and b.city = %s"
        cursor.execute(statement, [name,city])
        row = cursor.fetchall()
    return row

def search_by_cuisine(cuisine):
    with connection.cursor() as cursor:
        category = '%Restaurant%'
        # Search restaurants according to Cuisine
        statement = "SELECT b.name From business b where b.categories like %s and b.categories like %s"
        cursor.execute(statement, [category,cuisine])
        row = cursor.fetchall()

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
        statement = "SELECT * From (SELECT b.city as c,count(b.business_id) as cnt \
                     From business b group by b.city order by count(b.business_id) desc) where rownum<=5 \
                     UNION \
                     SELECT'others' as c,sum(cnt) as cnt FROM (SELECT count(b.business_id) as cnt From business b \
                     group by b.city order by count(b.business_id) desc offset 5 row)"
        cursor.execute(statement)
        row = cursor.fetchall()
    return row

def sql_business_open():
    with connection.cursor() as cursor:

        statement = "SELECT bc,count(bid),y,m from \
                    (SELECT b.business_id as bid, b.city as bc, \
                    extract(year from min(rd.review_date)) as y, extract(month from min(rd.review_date)) as m \
                    from business b, rateandreview r,reviewdates rd \
                    where b.business_id=r.r_id and r.r_id=rd.r_id and b.is_open=1 \
                    group by b.business_id, b.city ) \
                    where bc in (SELECT * From \
                    (SELECT b.city From business b group by b.city order by count(b.business_id) desc) where rownum<=5) \
                    group by y,m,bc \
                    order by y+m/100 asc"
        cursor.execute(statement)
        row = cursor.fetchall()

    return row

def sql_business_close():
    with connection.cursor() as cursor:

        statement = "SELECT bc,count(bid),y,m from \
                    (SELECT b.business_id as bid, b.city as bc, \
                    extract(year from max(rd.review_date)) as y, extract(month from max(rd.review_date)) as m \
                    from business b, rateandreview r,reviewdates rd \
                    where b.business_id=r.r_id and r.r_id=rd.r_id and b.is_open=0 \
                    group by b.business_id, b.city ) \
                    where bc in (SELECT * From \
                    (SELECT b.city From business b group by b.city order by count(b.business_id) desc) where rownum<=5) \
                    group by y,m,bc \
                    order by y+m/100 asc"
        cursor.execute(statement)
        row = cursor.fetchall()

    return row

def sql_average_monthly_rating():
    with connection.cursor() as cursor:
        c = ['%Resatuarant%','%Shopping%','%Home%','%Fitness%','%Arts%','%Health%']
        statement = "SELECT nvl(restaurant_avg,0) , nvl(shopping_avg,0) , nvl(home_avg,0), \
                    nvl(fitness_avg,0) ,nvl(arts_avg,0),nvl(health_avg,0), mon1 , yy1  from \
                    ((((((SELECT avg(rateandreview.rating) as restaurant_avg , \
                    extract(month from reviewdates.review_date) as mon2, \
                    extract(year from reviewdates.review_date) as yy2  \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) full outer join \
                    (SELECT avg(rateandreview.rating) as shopping_avg , \
                    extract(month from reviewdates.review_date) as mon1, \
                    extract(year from reviewdates.review_date) as yy1 \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) \
                    on mon1=mon2 and yy2=yy1)full outer join \
                    (SELECT avg(rateandreview.rating) as home_avg , \
                    extract(month from reviewdates.review_date) as mon3, \
                    extract(year from reviewdates.review_date) as yy3 \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) \
                    on mon1 = mon3 and yy1 = yy3) full outer join \
                    (SELECT avg(rateandreview.rating) as fitness_avg , \
                    extract(month from reviewdates.review_date) as mon4, \
                    extract(year from reviewdates.review_date) as yy4 \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) \
                    on mon1= mon4 and yy1 = yy4) full outer join \
                    (SELECT avg(rateandreview.rating) as arts_avg , \
                    extract(month from reviewdates.review_date) as mon5, \
                    extract(year from reviewdates.review_date) as yy5 \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) \
                    on mon1 = mon5 and yy1 = yy5) full outer join \
                    (SELECT avg(rateandreview.rating) as health_avg , \
                    extract(month from reviewdates.review_date) as mon6, \
                    extract(year from reviewdates.review_date) as yy6 \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) \
                    on mon1 = mon6 and yy1 = yy6)"
        cursor.execute(statement, [c[0],c[1],c[2],c[3],c[4],c[5]])
        row = cursor.fetchall()

    return row

def sql_average_monthly_rating_cuisine():

    with connection.cursor() as cursor:
        c = ['%American%','%Chinese%','%Japanese%','%Italian%','%Mexican%','%Thai%']
        statement = "SELECT nvl(restaurant_avg,0) , nvl(shopping_avg,0) , nvl(home_avg,0), \
                    nvl(fitness_avg,0) ,nvl(arts_avg,0),nvl(health_avg,0), mon1 , yy1  from \
                    ((((((SELECT avg(rateandreview.rating) as restaurant_avg , \
                    extract(month from reviewdates.review_date) as mon2, \
                    extract(year from reviewdates.review_date) as yy2  \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) full outer join \
                    (SELECT avg(rateandreview.rating) as shopping_avg , \
                    extract(month from reviewdates.review_date) as mon1, \
                    extract(year from reviewdates.review_date) as yy1 \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) \
                    on mon1=mon2 and yy2=yy1)full outer join \
                    (SELECT avg(rateandreview.rating) as home_avg , \
                    extract(month from reviewdates.review_date) as mon3, \
                    extract(year from reviewdates.review_date) as yy3 \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) \
                    on mon1 = mon3 and yy1 = yy3) full outer join \
                    (SELECT avg(rateandreview.rating) as fitness_avg , \
                    extract(month from reviewdates.review_date) as mon4, \
                    extract(year from reviewdates.review_date) as yy4 \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) \
                    on mon1= mon4 and yy1 = yy4) full outer join \
                    (SELECT avg(rateandreview.rating) as arts_avg , \
                    extract(month from reviewdates.review_date) as mon5, \
                    extract(year from reviewdates.review_date) as yy5 \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) \
                    on mon1 = mon5 and yy1 = yy5) full outer join \
                    (SELECT avg(rateandreview.rating) as health_avg , \
                    extract(month from reviewdates.review_date) as mon6, \
                    extract(year from reviewdates.review_date) as yy6 \
                    from reviewdates , rateandreview , business \
                    where reviewdates.r_id = rateandreview.r_id and \
                    rateandreview.business_id = business.business_id \
                    and business.categories like %s \
                    group by extract(year from reviewdates.review_date), \
                    extract(month from reviewdates.review_date) \
                    order by extract(year from reviewdates.review_date)) \
                    on mon1 = mon6 and yy1 = yy6)"
        cursor.execute(statement, [c[0],c[1],c[2],c[3],c[4],c[5]])
        row = cursor.fetchall()

    return row
# def login(request):
# 	return render(request, 'accounts/login.html')