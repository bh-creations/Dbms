from django.urls import path,include
from . import views
from feny.views import PieChartView
from feny.views import BarGraphView

urlpatterns = [
	path('', views.index, name='index'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('signup/', views.signup, name='signup'),
	path('piechart/', PieChartView.as_view(), name='piechart'),
	path('bargraph/', BarGraphView.as_view(), name='bargraph'),
]