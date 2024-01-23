
from django.urls import path
from . import views


urlpatterns = [
    path('ok/', views.ok_view, name='ok'),
    path('property_registration/step1/', views.step1_view, name='step1'),

    # path('api/property_registration/step1/<str:registrationId>/', views.step1_detail_view, name='step1_detail'),
    # path('api/property_registration/step2/<str:registrationId>/', views.step2_view, name='step2'),
    # path('api/property_registration/step3/<str:registrationId>/', views.step3_view, name='step3'),
    # path('api/property_registration/step4/<str:registrationId>/', views.step4_view, name='step4'),
    # path('api/property_registration/step5/<str:registrationId>/', views.step5_view, name='step5'),
    # path('api/property_registration/step6/<str:registrationId>/', views.step6_view, name='step6'),
    # path('api/property_registration/step7/<str:registrationId>/', views.step7_view, name='step7'),
]