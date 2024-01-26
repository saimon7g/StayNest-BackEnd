from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PropertyRegistration
from .serializers import PropertyRegistrationSerializer,LocationSerializer,SomeBasicsSerializer,PropertyStep2Serializer,PropertyStep3Serializer,PropertyStep4Serializer,PropertyStep5Serializer,PayingGuestSerializer,PropertyStep7Serializer


# Step 1 Views
def ok_view(request):
     return JsonResponse({"message": "Step ok view"})

@csrf_exempt
@api_view(['GET', 'POST'])
def step1_view(request):
    if request.method == 'GET':
        # You can handle GET requests here if needed
        return Response({"message": "This is a GET request."}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        try:
            data = request.data
            print(data)
            serializer = PropertyRegistrationSerializer(data=data)
           
            if serializer.is_valid():
                step1_instance = serializer.save()
                
            
                # You can customize the response as needed
                return Response({"registration_id": step1_instance.registration_id, "message": "Property registration step 1 completed."}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            import traceback
            traceback_str = traceback.format_exc()
            return Response({"error": str(e), "traceback": traceback_str}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT'])
def step2_view(request, registration_id):
    try:
        # Fetch Step 2 data from the session
        step2_data = request.session.get('step2_data', {})

        if request.method == 'GET':
            # Validate and serialize the data
            serializer = PropertyStep2Serializer(data=step2_data)

            if serializer.is_valid():
                # Return the serialized Step 2 data
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            data = request.data
            data['registration_id'] = registration_id  # Associate Step 2 with Step 1 using registration_id
            request.session['step2_data'] = data
            return Response({"message": "Property registration step 2 done","data":data,}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET', 'PUT'])
def step3_view(request, registration_id):
    try:
        # Fetch Step 2 data from the session
        step3_data = request.session.get('step3_data', {})

        if request.method == 'GET':
            # Validate and serialize the data
            serializer = PropertyStep3Serializer(data=step3_data)

            if serializer.is_valid():
                # Return the serialized Step 2 data
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            data = request.data
            data['registration'] = registration_id  # Associate Step 3 with Step 1 using registration_id
            request.session['step3_data'] = data
            return Response({"message": "Property registration step 3 done","data":data,}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET', 'PUT'])
def step4_view(request, registration_id):
    try:
        # Fetch Step 2 data from the session
        step4_data = request.session.get('step4_data', {})

        if request.method == 'GET':
            # Validate and serialize the data
            serializer = PropertyStep4Serializer(data=step4_data)

            if serializer.is_valid():
                # Return the serialized Step 2 data
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            data = request.data
            data['registration'] = registration_id  # Associate Step 3 with Step 1 using registration_id
            request.session['step4_data'] = data
            return Response({"message": "Property registration step 4 done","data":data,}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET', 'PUT'])
def step5_view(request, registration_id):
    try:
        # Fetch Step 2 data from the session
        step5_data = request.session.get('step5_data', {})

        if request.method == 'GET':
            # Validate and serialize the data
            serializer = PropertyStep5Serializer(data=step5_data)

            if serializer.is_valid():
                # Return the serialized Step 2 data
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            data = request.data
            data['registration'] = registration_id  # Associate Step 3 with Step 1 using registration_id
            request.session['step5_data'] = data
            return Response({"message": "Property registration step 5 done","data":data,}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET', 'PUT'])
def step6_view(request, registration_id):
    try:
        # Fetch Step 2 data from the session
        step6_data = request.session.get('step6_data', {})

        if request.method == 'GET':
            # Validate and serialize the data
            serializer =PayingGuestSerializer(data=step6_data)

            if serializer.is_valid():
                # Return the serialized Step 2 data
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            data = request.data
            data['registration'] = registration_id  # Associate Step 3 with Step 1 using registration_id
            request.session['step6_data'] = data
            return Response({"message": "Property registration step 6 done","data":data,}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@csrf_exempt
@api_view(['GET', 'PUT'])
def step7_view(request, registration_id):
    try:
        # Fetch Step 2 data from the session
        # step7_data = request.session.get('step7_data', {})
        step7_data = request.data
        

        if request.method == 'GET':
            # Validate and serialize the data
            serializer =PropertyStep7Serializer(data=step7_data)

            if serializer.is_valid():
                # Return the serialized Step 2 data
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            # Write data for previous steps to the database
            # Step 2
            # step2_data=request.session['step2_data']
            # # step2_data['registration_id'] =registration_id
            # print(step2_data)
            # serializer_step2 = PropertyStep2Serializer(data=step2_data)
            
            # if serializer_step2.is_valid():
            #     serializer_step2.save()
            # else:
            #     print('not valid 2')
                
            #     print(serializer_step2.errors)
                

            # Step 3
            # step3_data=request.session['step3_data']
            # step3_data['registration_id'] = registration_id
            # serializer_step3 = PropertyStep3Serializer(data=step3_data)
            # if serializer_step3.is_valid():
            #     serializer_step3.save()
            # else:
            #     print('not valid 3')
                
            #     print(serializer_step3.errors)
            # # Step 4
            # step4_data=request.session['step4_data']
            # step4_data['registration_id'] = registration_id
            # serializer_step4 = PropertyStep4Serializer(data=step4_data)
            # if serializer_step4.is_valid():
            #     serializer_step4.save()
            # else:
            #     print('error ',step4_data)
            #     return Response(serializer_step4.errors, status=status.HTTP_400_BAD_REQUEST)

            # Step 5
            # step5_data=request.session['step5_data']
            # if step5_data:
            #     step5_data['registration_id'] = registration_id
            #     # print(step5_data)
            #     serializer_step5 = PropertyStep5Serializer(data=step5_data)
            #     if serializer_step5.is_valid():
                    
            #         print('data paiso??')
            #         serializer_step5.save()
            #     else: 
            #         return Response(serializer_step5.errors, status=status.HTTP_400_BAD_REQUEST)
            # Step 6
            # step6_data=request.session['step6_data']
            # if step6_data:
            #     step6_data['registration_id'] = registration_id
            #     serializer_step6 = PayingGuestSerializer(data=step6_data)
            #     if serializer_step6.is_valid():
            #         serializer_step6.save()
            #     else:
            #          return Response(serializer_step6.errors, status=status.HTTP_400_BAD_REQUEST)


            # Step 7
            step7_data['registration_id'] = registration_id
            serializer_step7 = PropertyStep7Serializer(data=step7_data)
            if serializer_step7.is_valid():
                serializer_step7.save()
            else:
                return Response(serializer_step7.errors, status=status.HTTP_400_BAD_REQUEST)

            # # Optionally, you can clear the session data for all steps after saving to the database
            # del request.session['step1_data']
            # del request.session['step2_data']
            # del request.session['step3_data']
            # del request.session['step4_data']
            # del request.session['step5_data']
            # del request.session['step6_data']
            # del request.session['step7_data']

            return Response({"message": "Property registration steps 1 to 7 done"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)