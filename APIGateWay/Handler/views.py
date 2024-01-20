from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def HomeData(request):
    res={
        "data":"Hello World from Handler Home Data"
        
    }
    return JsonResponse(res)
def test(request):
    res={
        "data":"Hello World from Handler test"
    }
    return JsonResponse(res)
