
from django.urls import path
from . import views


urlpatterns = [
    path('notification/', views.notify_guest, name='test'),   
]