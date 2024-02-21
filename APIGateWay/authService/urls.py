from django.urls import path
from .views import LoginView, SignupView,logout,HostSignupView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('hostsignup/', HostSignupView.as_view(), name='hostsignup'),
    path('logout/', logout, name='logout'),
    # path('test/', TestView.as_view(), name='test'),   
]
