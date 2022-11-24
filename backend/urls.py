from django.urls import path
from backend import views


urlpatterns = [ 
    path('', views.HomeView, name='homeview'),
    path('search/', views.SearchView, name="searchview"),
    path('error?=<str:errorType>&text=<path:errorText>', views.ErrorView, name="errorview")
] 
