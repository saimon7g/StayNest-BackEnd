from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

# Step 1 Views
def ok_view(request):
     return JsonResponse({"message": "Step ok view"})

@csrf_exempt
def step1_view(request):
    if request.method == 'GET':
        # Implement logic for handling GET request for step 1
        return JsonResponse({"message": "Step 1 GET view"})
    elif request.method == 'POST':
        # Implement logic for handling POST request for step 1
        return JsonResponse({"registrationId": "unique_registration_id", "message": "Property registration step 1 completed."}, status=201)
