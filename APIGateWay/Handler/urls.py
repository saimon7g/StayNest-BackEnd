from django.urls import path
from . import views 
from .views import RedirectHostView,RedirectGuestView
from django.views.generic import RedirectView


urlpatterns = [
    path('test/', views.hello_view, name='hello'),
    path('HomeData/', views.HomeData, name='HomeData'),
    path('host/<path:path>/', RedirectHostView.as_view(), name='custom_redirect'),
    path('guest/<path:path>/', RedirectGuestView.as_view(), name='custom_redirect'),

    # path('host/',RedirectView.as_view(url='http://localhost:8080/'))
    
    # Add more URL patterns as needed
]
