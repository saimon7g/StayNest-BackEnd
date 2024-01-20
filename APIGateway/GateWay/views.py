from django.http import JsonResponse

# Create your views here.
def hello_view(request):
    data={"name":"Hello World from APIGateway Hello"}
    print("Hello World")
    # only data from backend with success and status code
    return JsonResponse(data,status=200)

def HomeData(request):
    data={"name":"Hello World from APIGateway Home Data"}
    print("Hello World")
    # only data from backend with success and status code
    return JsonResponse(data,status=200)
