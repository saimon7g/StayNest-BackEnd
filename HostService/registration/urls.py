
from django.urls import path
from . import views


urlpatterns = [
    path('ok/', views.test_token, name='test'),
    path('complete_registration/<str:registration_id>/', views.complete_registration_view, name='complete'),
    path('property_registration/step1/', views.step1_view, name='step1'),

    #path('property_registration/step1/<str:registration_id>/', views.step1_detail_view, name='step1_detail'),
    path('property_registration/step2/<str:registration_id>/', views.step2_view, name='step2'),
    path('property_registration/step3/<str:registration_id>/', views.step3_view, name='step3'),
    path('property_registration/step4/<str:registration_id>/', views.step4_view, name='step4'),
    path('property_registration/step5/<str:registration_id>/', views.step5_view, name='step5'),
    path('property_registration/step6/<str:registration_id>/', views.step6_view, name='step6'),
    path('property_registration/step7/<str:registration_id>/', views.step7_view, name='step7'),
]