from django.shortcuts import render

# Create your views here.
#notifying the guest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import GuestNotification
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework.decorators import api_view

@csrf_exempt
@login_required
@api_view(['POST'])
def notify_guest(request):
    if request.method == 'POST':
        message = request.data['message']
        guest = User.objects.get(username=request.data['guest'])
        notification = GuestNotification(user=guest, message=message)
        notification.save()
        return JsonResponse({'message': 'Notification sent successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)