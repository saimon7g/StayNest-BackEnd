from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.hello_view, name='hello'),
    path('HomeData/', views.HomeData, name='HomeData'),
    
    # Add more URL patterns as needed
]
