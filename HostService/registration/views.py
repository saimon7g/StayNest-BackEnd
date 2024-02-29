from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from django.utils import timezone
from .models import (PropertyRegistration,PropertyStep2,PropertyStep3,PropertyStep4,PropertyStep5,PayingGuest,
                     PropertyStep7,SelectedDate,PropertyReview,Location)
from .serializers import (PropertyRegistrationSerializer,LocationSerializer,SomeBasicsSerializer,PropertyStep2Serializer,
                          PropertyStep3Serializer,PropertyStep4Serializer,PropertyStep5Serializer,PayingGuestSerializer,
                          PropertyStep7Serializer,CompleteRegistrationSerializer,ConcisePropertySerializer,SelectedDateSerializer,
                          DetailedPropertySerializer,PayingGuestSerializer,PropertyReviewSerializer,
                          BookedPropertyDetailsSerializer)
                          


from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.decorators import  authentication_classes, permission_classes

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
import json
from datetime import datetime,timedelta
from django.core import serializers

def getUserByToken(request):
    auth_header = request.headers.get('Authorization')
    print(auth_header)
    if auth_header and auth_header.startswith('Token '):
        # Extract the token from the Authorization header
        token_key = auth_header.split(' ')[1]

        try:
            # Retrieve the Token object using the token key
            token = Token.objects.get(key=token_key)

            # Assuming Token model has a user foreign key field named 'user'
            user_id = token.user.id
            return user_id
        except Token.DoesNotExist:
            # Handle the case where the token is not found
            return -1

    else:
        # Authentication header is missing or invalid
        return -1
def update_intervals_and_mark_unavailable(arg_interval, property_step7):
    selected_dates = property_step7.selected_dates.all()
    print(selected_dates)
    updated_intervals = []
    
    for interval in selected_dates:
        if arg_interval.start_date >= interval.start_date and arg_interval.end_date <= interval.end_date:
            if interval.status == 'unavailable':
                return False
            print('interval.start_date',interval.start_date)
            if arg_interval.start_date > interval.start_date:

                # Create a new interval for the available period before arg_interval
                new_interval_before = SelectedDate.objects.create(start_date=interval.start_date, end_date=(arg_interval.start_date - timedelta(days=1)), status='available')
                updated_intervals.append(new_interval_before)

                
            # Create a new interval for the unavailable period corresponding to arg_interval
            new_interval_unavailable = SelectedDate.objects.create(start_date=arg_interval.start_date, end_date=arg_interval.end_date, status='unavailable')
            updated_intervals.append(new_interval_unavailable)
            
            if arg_interval.end_date < interval.end_date:
                # Create a new interval for the available period after arg_interval
                new_interval_after = SelectedDate.objects.create(start_date=(arg_interval.end_date + timedelta(days=1)), end_date=interval.end_date, status='available')
                updated_intervals.append(new_interval_after)
                
            # Remove the original interval from the selected_dates queryset
            interval.delete()
        else:
            # If the arg_interval does not fit within the current interval, keep the interval unchanged
            updated_intervals.append(interval)

    # Add all the updated intervals to the property_step7.selected_dates
    property_step7.selected_dates.add(*updated_intervals)
    return True

# Usage example:
# Assuming arg_interval and property_step7 are defined elsewhere
# update_intervals_and_mark_unavailable(arg_interval, property_step7)
def mark_available(registration_id,start_date,end_date):
    # Fetch the PropertyStep7 instance using the registration_id
    try:
        property_step7 = PropertyStep7.objects.get(registration_id=registration_id)
    except PropertyStep7.DoesNotExist:
        print('PropertyStep7 instance not found for the provided registration_id')
        return False
    print(start_date)
    # Create a SelectedDate instance from the arg_interval data
    arg_interval = SelectedDate(start_date=start_date, end_date=end_date)
    
    print(arg_interval)
    try:
        #  if a interval in the selected_dates queryset matches with the arg_interval
        #  and status is 'unavailable', make the interval 'available'

        selected_dates = property_step7.selected_dates.all()
        for interval in selected_dates:
            if arg_interval.start_date == interval.start_date and arg_interval.end_date == interval.end_date:
                if interval.status == 'unavailable':
                    interval.status = 'available'
                    interval.save()
                    return True
                else:
                    return True
        return False
    except:
        return False
    


@api_view(['GET'])

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
            print(auth_header)
            if auth_header and auth_header.startswith('Token '):
                # Extract the token from the Authorization header
                token_key = auth_header.split(' ')[1]

                try:
                    # Retrieve the Token object using the token key
                    token = Token.objects.get(key=token_key)

                    # Assuming Token model has a user foreign key field named 'user'
                    user_id = token.user.id
                    print(request.data)
                    # Check if the user is in the 'host' group
                    if token.user.groups.filter(name='host').exists():
                        serializer = PropertyRegistrationSerializer(data={**request.data, 'user': user_id})

                        if serializer.is_valid():
                            step1_instance = serializer.save()
                            return Response({"registration_id": step1_instance.registration_id, "message": "Property registration step 1 completed."}, status=status.HTTP_201_CREATED)
                        else:
                            print(serializer.errors)
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
            print("Error processing POST request ",traceback_str)
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


def step5_view(request, registration_id):
    try:    
        if request.method == 'GET':
            step5_data_session = request.session.get('step5_data', {})
            if step5_data_session:
                serializer = PropertyStep5Serializer(data=step5_data_session)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
            try:
                property_step5 = PropertyStep5.objects.get(registration_id=registration_id)
                serializer = PropertyStep5Serializer(instance=property_step5)
                print('serializer',json.dumps(serializer.data)  )
                data= json.dumps(serializer.data)

                return Response(data, status=status.HTTP_200_OK)
            except PropertyStep5.DoesNotExist:
                # If step5 data is not in the session or database, return an error
                return Response({"error": "Property step5 data not found."}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'PUT':

           
            data = request.data
            data['registration_id'] = registration_id  
            try:
                # Check if entry exists
                property_step5 = PropertyStep5.objects.get(registration_id=registration_id)
                property_step5.delete()  # Delete existing entry
            except PropertyStep5.DoesNotExist:
                pass  # Entry does not exist, proceed to create a new one
            print('data',data['breakfast'])
            serializer = PropertyStep5Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "Property registration step 5 updated successfully"}, status=200)
            else:
                print('error',serializer.errors)
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
@api_view(['GET','PUT'])
@permission_classes([AllowAny])
def properties_by_type_view(request):
    if request.method == 'GET':
        return Response({"Message":"properties_by_type_view"})
    if request.method == 'PUT':
        type = request.data['online_type']
        properties = PropertyRegistration.objects.filter(
            status='completed',
            online_type=type
        ).distinct()  # Get distinct properties
        serialized_properties = ConcisePropertySerializer(properties, many=True).data
        return Response({"results": serialized_properties})
    
@api_view(['GET'])
@permission_classes([AllowAny])
def my_listings_view(request):
    if request.method == 'GET':
        host_id = getUserByToken(request)
        print('host_id',host_id)
        

        properties = PropertyRegistration.objects.filter(
            status='completed',
            user=host_id).distinct()  # Get distinct properties
        serialized_properties = ConcisePropertySerializer(properties, many=True).data
        return Response(serialized_properties)
             
@api_view(['GET','PUT'])
@permission_classes([AllowAny])
#  search_properties_view, name='search_properties'),
def search_properties_view(request):
    category = request.data.get('category', 'any')


    # Access the 'min' and 'max' keys of the 'price_range' dictionary
    

    # Get properties with selected dates that overlap with the given check-in and check-out dates
    if category == 'any':
        properties = PropertyRegistration.objects.filter(
            status='completed',
            step7__selected_dates__end_date__gte=date.today(),  # Selected date start before or on check-out date
        ).distinct()  # Get distinct properties
        serialized_properties = ConcisePropertySerializer(properties, many=True).data
        return Response({"results": serialized_properties}) 
    else:
        location = request.data['location']
        print('location',location)
        # guests = request.GET.get('guests')
        guests = request.data['guests']
        room_type = request.data['room_type']
        # Get the 'price_range' query parameter
        price_range = request.data['price_range']
        price_range_min = price_range['min']    
        price_range_max = price_range['max']
        check_in = datetime.strptime(request.data['check_in'], '%Y-%m-%d').date()
        check_out = datetime.strptime(request.data['check_out'], '%Y-%m-%d').date()
        properties = PropertyRegistration.objects.filter(
            status='completed',
            # location__selected_location=location, 
            step7__selected_dates__start_date__lte=check_in,  # Selected date start before or on check-out date
            step7__selected_dates__end_date__gte=check_out  # Selected date end after or on check-in date
        ).distinct()  # Get distinct properties
        serialized_properties = ConcisePropertySerializer (properties, many=True).data

        property_list = []
        for property in serialized_properties:
            registration_id = property['property_id'] 
            property_step7 = PropertyStep7.objects.get(registration_id=registration_id)
            selected_dates = property_step7.selected_dates.filter(
                start_date__gte=check_in, end_date__lte=check_out, status='available'
            ).order_by('start_date')
            if selected_dates:
                interval = selected_dates.first()
                property['availability'] = SelectedDateSerializer(interval).data
                property_list.append(property)
        return Response({"results": property_list})



@api_view(['GET'])
@permission_classes([AllowAny])
#  search_properties_view, name='search_properties'),
def property_details_view(request,property_id):
    try:
        registration_instance = PropertyRegistration.objects.get(registration_id=property_id)
    except PropertyRegistration.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer =DetailedPropertySerializer (registration_instance)

    data=serializer.data
    
    return Response(data, status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([AllowAny])
def property_dashboard_view(request,property_id):
    try:
        registration_instance = PropertyRegistration.objects.get(registration_id=property_id)
    except PropertyRegistration.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookedPropertyDetailsSerializer(registration_instance)

    data=serializer.data
    
    return Response(data, status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([AllowAny])
#  search_properties_view, name='search_properties'),
def step1_detail_view(request,registration_id):
    
    return Response({"Message":"step1_detail_view"})


@api_view(['GET','POST'])
def property_availability_view(request,property_id):
    if request.method == 'GET':
        try:
            property_step7 = PropertyStep7.objects.get(registration_id=property_id)
            serializer = PropertyStep7Serializer(property_step7)
            return Response(serializer.data['selected_dates'], status=status.HTTP_200_OK)
        except PropertyStep7.DoesNotExist:
            return Response({"error": "PropertyStep7 instance not found for the provided registration_id"}, status=404)
    if request.method == 'POST':
        # Retrieve registration_id from request data
        registration_id = property_id

        # Fetch the PropertyStep7 instance using the registration_id
        try:
            property_step7 = PropertyStep7.objects.get(registration_id=registration_id)
        except PropertyStep7.DoesNotExist:
            return Response({"message": "PropertyStep7 instance not found for the provided registration_id"}, status=404)

        # Create a SelectedDate instance from the arg_interval data
        arg_interval_start_date = request.data['start_date']
        arg_interval_end_date = request.data['end_date']
        arg_interval = SelectedDate(start_date=datetime.strptime(arg_interval_start_date, '%Y-%m-%d').date(),
                                end_date=datetime.strptime(arg_interval_end_date, '%Y-%m-%d').date())

        try:
            updated=update_intervals_and_mark_unavailable(arg_interval, property_step7)
            if updated:
                return Response({"message": "Intervals updated successfully"}, status=200)
            else:
                return Response({"message": "Intervals not updated"}, status=status.HTTP_409_CONFLICT)
            
        except:
            return Response({"message": "No intervals updated"})
    

@api_view(['GET', 'POST']) 
def mark_interval_available_view(request,property_id):
    if request.method == 'GET':
        return Response({"Message":"mark_interval_available_view"})
    if request.method == 'POST':
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        marked=mark_available(property_id,start_date,end_date)
        if marked:
            return Response({"message": "Interval marked as available"}, status=200)
        else:
            return Response({"message": "Interval not marked as available"}, status=status.HTTP_409_CONFLICT)
        
        
@api_view(['GET', 'POST'])


def review_view(request, property_id):
    # Get the property registration object
    

    if request.method == 'GET':
        # Retrieve all reviews for the property
        reviews = PropertyReview.objects.filter(property_id=property_id)
        serializer = PropertyReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new review for the property
        serializer = PropertyReviewSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure the requesting user is the owner of the property
            property_registration = PropertyRegistration.objects.get(registration_id=property_id)
            if request.user == property_registration.user:
                serializer.save(property_id=property_registration, user_id=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "You are not authorized to review this property."},
                                status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def profile_view(request):
    # Retrieve host profile
    return Response({})


@api_view(['GET', 'POST'])
def property_review_list(request, property_id):
    if request.method == 'GET':
        property_reviews = PropertyReview.objects.filter(property_id=property_id)
        serializer = PropertyReviewSerializer(property_reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        request.data['property_id'] = property_id  # Ensure property_id is set in the request data
        serializer = PropertyReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)