from django.urls import path,include
from . import views
from feny.views import Pie_Popular_City,Bar_Category_Percentage, Pie_Review_Distribution, Line_Month_Review_Star


urlpatterns = [
	path('', views.index, name='index'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('signup/', views.signup, name='signup'),
	path('piechart/', Pie_Popular_City.as_view(), name='piechart'),
	path('piechart2/', Pie_Review_Distribution.as_view(), name='piechart2'),
	path('bargraph/', Bar_Category_Percentage.as_view(), name='bargraph'),
	path('linechart/', Line_Month_Review_Star.as_view(), name='linechart'),
]