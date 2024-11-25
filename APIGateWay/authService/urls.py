from django.urls import path
from .views import LoginView, SignupView,logout,HostSignupView,HostProfileView,GuestProfileView,HostProfileDetailsView,UserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('hostsignup/', HostSignupView.as_view(), name='hostsignup'),
    path('logout/', logout, name='logout'),
    path('host_profile/<int:uid>/', HostProfileView.as_view(), name='host_profile'),
    path('host_profile_details/<int:uid>/', HostProfileDetailsView.as_view(), name='guest_profile_details'),
    path('guest_profile/<int:uid>/', GuestProfileView.as_view(), name='guest_profile'),
    path('user/', UserView.as_view(), name='user'),
]
