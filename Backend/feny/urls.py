from django.urls import path,include
from . import views
from feny.views import *


urlpatterns = [
	path('', views.index, name='index'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('signup/', views.signup, name='signup'),
	path('piechart/', Pie_Popular_City.as_view(), name='piechart'),
	path('piechart2/', Pie_Review_Distribution.as_view(), name='piechart2'),
	path('bargraph/', Bar_Category_Percentage.as_view(), name='bargraph'),
	path('linechart/', Line_Month_Review_Star.as_view(), name='linechart'),
	path('linechart2/', Line_Business_Open.as_view(), name='linechart2'),
	path('linechart3/', Line_Business_Close.as_view(), name='linechart3'),
	path('linechart4/', Average_Monthly_Rating.as_view(), name='linechart4'),
	path('linechart5/', Average_Monthly_Rating_Cuisine.as_view(), name='linechart5'),
]