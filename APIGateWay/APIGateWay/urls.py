"""
URL configuration for APIGateWay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView

def custom_redirect(request, path):
    # Construct the target URL by appending the original path to http://localhost:8080/
    target_url = f'http://localhost:8080/{path}'
    return RedirectView.as_view(url=target_url)(request)

urlpatterns = [
    path('admin/', admin.site.urls),# admin
    path('host/<path:path>/', custom_redirect, name='custom_redirect'),
    path('', include('Handler.urls')),# Handler
]
