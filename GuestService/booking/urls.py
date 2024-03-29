
from django.urls import path
from . import views


urlpatterns = [   
    path('notification/', views.notify_guest, name='test'),  

    path('book/', views.book_view, name='book'),
    path('booking/<str:booking_id>/', views.booking_view, name='booking'),
    path('booking/<str:booking_id>/status/', views.booking_status_view, name='booking_status'),
    path('reserve/', views.reserve, name='reserve'),
    path('reservation/<str:reservation_id>/', views.get_reservation, name='reservation'),
    path('booking/<str:booking_id>/payment/', views.payment_view, name='payment'),
    path('booking/<str:booking_id>/payment/<str:payment_id>/', views.payment_with_id_view, name='payment_with_id'),
    path('upcoming_bookings/', views.upcoming_bookings, name='upcoming_bookings'),
]
 