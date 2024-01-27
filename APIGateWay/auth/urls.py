from django.urls import path
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('test/',views.test_token,name='test')    
]
