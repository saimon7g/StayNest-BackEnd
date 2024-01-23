
from django.urls import path
from . import views

urlpatterns = [
    path('ok/', views.ok_view, name='ok'),
   
]