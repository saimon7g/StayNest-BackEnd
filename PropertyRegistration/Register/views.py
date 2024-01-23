from django.shortcuts import render
from django.http import JsonResponse
def ok_view(request):
    result ={
        'message': 'Hello, ok!',
    }
    return JsonResponse(result)

