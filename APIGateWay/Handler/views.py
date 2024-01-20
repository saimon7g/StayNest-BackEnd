from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def hello_view(request):
    result ={
        
        
        'message': 'Hello, World from APIGateWay Handler hello_view()',
    }
    return JsonResponse(result)

def HomeData(request):
    result ={
        
        
        'message': 'Hello, World from APIGateWay Handler HomeData()',
    }
    return JsonResponse(result)