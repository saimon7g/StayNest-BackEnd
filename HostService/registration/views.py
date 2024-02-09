from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import (PropertyRegistration,PropertyStep2,PropertyStep3,PropertyStep4,PropertyStep5,PayingGuest,PropertyStep7)
from .serializers import (PropertyRegistrationSerializer,LocationSerializer,SomeBasicsSerializer,PropertyStep2Serializer,
                          PropertyStep3Serializer,PropertyStep4Serializer,PropertyStep5Serializer,PayingGuestSerializer,
                          PropertyStep7Serializer,CompleteRegistrationSerializer)


from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.decorators import  authentication_classes, permission_classes

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
import json
# Step 1 Views
def ok_view(request):
     return JsonResponse({"message": "Step ok view"})

class IsHostGroup(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='host').exists()

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def step1_view(request):
    if request.method == 'GET':
        try:
            # Allow any authenticated user to make a GET request
            return Response({"message": "This is a GET request",}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Error processing GET request"})

    elif request.method == 'POST':
        try:
            auth_header = request.headers.get('Authorization')

            if auth_header and auth_header.startswith('Token '):
                # Extract the token from the Authorization header
                token_key = auth_header.split(' ')[1]

                try:
                    # Retrieve the Token object using the token key
                    token = Token.objects.get(key=token_key)

                    # Assuming Token model has a user foreign key field named 'user'
                    user_id = token.user.id

                    # Check if the user is in the 'host' group
                    if token.user.groups.filter(name='host').exists():
                        serializer = PropertyRegistrationSerializer(data={**request.data, 'user': user_id})

                        if serializer.is_valid():
                            step1_instance = serializer.save()
                            return Response({"registration_id": step1_instance.registration_id, "message": "Property registration step 1 completed."}, status=status.HTTP_201_CREATED)
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        # User is authenticated, but not in the 'host' group
                        print('---- not host')
                        return Response({"error": "User does not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

                except Token.DoesNotExist:
                    # Handle the case where the token is not found
                    return Response({"error": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)

            else:
                # Authentication header is missing or invalid
                return Response({"error": "Authentication required. Please log in."}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            import traceback
            traceback_str = traceback.format_exc()
            print("Error processing POST request")
            return Response({"error": str(e), "traceback": traceback_str}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@csrf_exempt
@api_view(['GET', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsHostGroup])
def step2_view(request, registration_id):
    try:    
        if request.method == 'GET':
            # Check if step2 data is in the session
            step2_data_session = request.session.get('step2_data', {})
            if step2_data_session:
                serializer = PropertyStep2Serializer(data=step2_data_session)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # If step2 data is not in the session, check if it's in the database
            try:
                property_step2 = PropertyStep2.objects.get(registration_id=registration_id)
                serializer = PropertyStep2Serializer(instance=property_step2)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PropertyStep2.DoesNotExist:
                # If step2 data is not in the session or database, return an error
                return Response({"error": "Property step2 data not found."}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'PUT':
            data = request.data
            data['registration_id'] = registration_id
            try:
                # Check if entry exists
                property_step2 = PropertyStep2.objects.get(registration_id=registration_id)
                property_step2.delete()  # Delete existing entry
            except PropertyStep2.DoesNotExist:
                pass  # Entry does not exist, proceed to create a new one

            serializer = PropertyStep2Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "Property registration step 2 updated successfully"}, status=200)
            else:
                return JsonResponse(serializer.errors, status=400)

        else:
            
            return Response({"error": "Invalid request method. Only GET/ PUT is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        print('error',e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
@csrf_exempt
@api_view(['GET', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsHostGroup])
def step3_view(request, registration_id):
    try:    
        if request.method == 'GET':
            step3_data_session = request.session.get('step3_data', {})
            print('step3_data_session',step3_data_session)
            if step3_data_session:
                serializer = PropertyStep3Serializer(data=step3_data_session)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
            # If step3 data is not in the session, check if it's in the database
            try:
                property_step3 = PropertyStep3.objects.get(registration_id=registration_id)
                serializer = PropertyStep3Serializer(instance=property_step3)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PropertyStep3.DoesNotExist:
                # If step3 data is not in the session or database, return an error
                return Response({"error": "Property step3 data not found."}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'PUT':
            data = request.data
            data['registration_id'] = registration_id  
            try:
                # Check if entry exists
                property_step3 = PropertyStep3.objects.get(registration_id=registration_id)
                property_step3.delete()  # Delete existing entry
            except PropertyStep3.DoesNotExist:
                pass  # Entry does not exist, proceed to create a new one

            serializer = PropertyStep3Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "Property registration step 2 updated successfully"}, status=200)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

@csrf_exempt
@api_view(['GET', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsHostGroup])
def step4_view(request, registration_id):
    try:    
        if request.method == 'GET':
            # Check if step4 data is in the session
            step4_data_session = request.session.get('step4_data', {})
            if step4_data_session:
                serializer = PropertyStep4Serializer(data=step4_data_session)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
            # If step4 data is not in the session, check if it's in the database
            try:
                property_step4 = PropertyStep4.objects.get(registration_id=registration_id)
                serializer = PropertyStep4Serializer(instance=property_step4)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PropertyStep4.DoesNotExist:
                # If step4 data is not in the session or database, return an error
                return Response({"error": "Property step4 data not found."}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'PUT':

           
            data = request.data
            data['registration_id'] = registration_id  
            try:
                # Check if entry exists
                property_step4 = PropertyStep4.objects.get(registration_id=registration_id)
                property_step4.delete()  # Delete existing entry
            except PropertyStep4.DoesNotExist:
                pass  # Entry does not exist, proceed to create a new one

            serializer = PropertyStep4Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "Property registration step 4 updated successfully"}, status=200)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    
@csrf_exempt
@api_view(['GET', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsHostGroup])
def step5_view(request, registration_id):
    try:    
        if request.method == 'GET':
            # Check if step5 data is in the session
            step5_data_session = request.session.get('step5_data', {})
            if step5_data_session:
                serializer = PropertyStep5Serializer(data=step5_data_session)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
            # If step5 data is not in the session, check if it's in the database
            try:
                property_step5 = PropertyStep5.objects.get(registration_id=registration_id)
                serializer = PropertyStep5Serializer(instance=property_step5)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PropertyStep5.DoesNotExist:
                # If step5 data is not in the session or database, return an error
                return Response({"error": "Property step5 data not found."}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'PUT':
            data = request.data
            data['registration_id'] = registration_id  

            # Save the data in the session
            request.session['step5_data'] = data

            return Response({"message": "Property registration step 2 done", "data": data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
@csrf_exempt
@api_view(['GET', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsHostGroup])
def step6_view(request, registration_id):
    try:    
        if request.method == 'GET':
            # Check if step6 data is in the session
            step6_data_session = request.session.get('step6_data', {})
            if step6_data_session:
                serializer = PayingGuestSerializer(data=step6_data_session)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
            # If step6 data is not in the session, check if it's in the database
            try:
                property_step6 = PayingGuest.objects.get(registration_id=registration_id)
                serializer = PayingGuestSerializer(instance=property_step6)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PayingGuest.DoesNotExist:
                return Response({"error": "Property step6 data not found."}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'PUT':

            data = request.data
            data['registration_id'] = registration_id  
            try:
                # Check if entry exists
                property_step6 = PayingGuest.objects.get(registration_id=registration_id)
                property_step6.delete()  # Delete existing entry
            except PayingGuest.DoesNotExist:
                pass  # Entry does not exist, proceed to create a new one

            serializer = PayingGuestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "Property registration step 6 updated successfully"}, status=200)
            else:
                print('error',serializer.errors)
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

@csrf_exempt
@api_view(['GET', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsHostGroup])
def step7_view(request, registration_id):
    try:
        step7_data = request.data
        # Check if step6 data is in the session
        if request.method == 'GET':
            step7_data_session = request.session.get('step7_data', {})
            if step7_data_session:
                serializer = PropertyStep7Serializer(data=step7_data_session)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
            # If step7 data is not in the session, check if it's in the database
            try:
                property_step7 = PropertyStep7.objects.get(registration_id=registration_id)
                serializer = PropertyStep7Serializer(instance=property_step7)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PropertyStep7.DoesNotExist:
                return Response({"error": "Property step7 data not found."}, status=status.HTTP_404_NOT_FOUND)

        elif request.method == 'PUT':
            data = request.data
            data['registration_id'] = registration_id
            try:
                # Check if entry exists
                property_step7 = PropertyStep7.objects.get(registration_id=registration_id)
                property_step7.delete()  # Delete existing entry
            except PropertyStep7.DoesNotExist:
                pass
            serializer = PropertyStep7Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                PropertyRegistration.objects.get(registration_id=registration_id).mark_as_completed()
                return JsonResponse({"message": "Property registration step 7 updated successfully"}, status=200)
            else:
                print('error',serializer.errors)
                return JsonResponse(serializer.errors, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt 
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")

@api_view(['GET'])
def complete_registration_view(request, registration_id):
    try:
        registration_instance = PropertyRegistration.objects.get(registration_id=registration_id)
    except PropertyRegistration.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CompleteRegistrationSerializer(registration_instance)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
#  search_properties_view, name='search_properties'),
def search_properties_view(request):
        
        return Response({"Message":"step1_detail_view"})



@api_view(['GET'])
@permission_classes([AllowAny])
#  search_properties_view, name='search_properties'),
def property_details_view(request):
    
    return Response({"Message":"property_detail_view"})
  
@api_view(['GET'])
@permission_classes([AllowAny])
#  search_properties_view, name='search_properties'),
def step1_detail_view(request,registration_id):
    
    return Response({"Message":"step1_detail_view"})
    
