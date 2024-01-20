from django.urls import path
from . import views

urlpatterns = [
    
    path('HomeData', views.HomeData, name='HomeData'),
    path('test', views.test, name='test'),
    
]
