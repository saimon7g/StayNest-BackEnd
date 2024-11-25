
from django.urls import path
from . import views


urlpatterns = [   
    path('notification/', views.notify_guest, name='test'),  

    path('book/', views.book_view, name='book'),
    path('booking_details/<str:booking_id>/', views.booking_view, name='booking'),
    path('booking/<str:booking_id>/status/', views.booking_status_view, name='booking_status'),
    path('reserve/', views.reserve, name='reserve'),
    path('reservation/<str:reservation_id>/', views.get_reservation, name='reservation'),
    path('booking/<str:booking_id>/payment/', views.payment_view, name='payment'),
    path('booking/<str:booking_id>/payment/<str:payment_id>/', views.payment_with_id_view, name='payment_with_id'),
    path('upcoming_bookings/as_guest/', views.upcoming_bookings_as_guest, name='upcoming_bookings'),
    path('upcoming_bookings/as_host/', views.upcoming_bookings_as_host, name='upcoming_bookings_as_host'),
]
 