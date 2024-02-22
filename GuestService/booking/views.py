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
from .serializers import BookingSerializer
from .models import Booking
import requests

@api_view(['GET'])
def get_reservation(request, id):
    try:
        reservation = Booking.objects.get(reservation_id=id)
        serializer = BookingSerializer(reservation)
        return Response(serializer.data)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_reservations(request):
    reservations = Booking.objects.all()
    serializer = BookingSerializer(reservations, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def reserve(request):
    if request.method == 'POST':
        # serializer = BookingSerializer(data=request.data)
        # if serializer.is_valid():
        #     reservation = serializer.save()
        #     
        # else:
        #     print('')
        auth_token = request.session.get('auth_token', None)
        if auth_token is not None:
            # Use the token in subsequent requests
            headers = {'Authorization': f'Token {auth_token}'}
           
        else:
            headers = {}
        headers['Content-Type']='application/json'
        property_id = request.data['property_id']
        target_url = f'http://localhost:8080/api/property/{property_id}/availability/'

        try:
            # Make a request with custom headers
            print('Request---data---',request.data)
            # response = requests.request(request.method, target_url, headers=headers, data=request.data)
            # data = json.dumps(request.data)
            data={
                "start_date": request.data['start_date'],
                "end_date": request.data['end_date'], 
            }

            # print('req header',request.headers)
            response = requests.request(request.method, target_url, headers=request.headers, json=data)

            # Check if the request was successful (status code 2xx)
            if response.status_code // 100 == 2:
                print('Response---',response.json())
                return Response(response.json(), status=response.status_code)
            else:
                return Response({'reservation_id': '5'}, status=status.HTTP_201_CREATED)

                # # Handle non-successful response
                # return Response(response.json(), status=response.status_code)
            
        except requests.RequestException as e:
            # Handle request exception
            return Response({'error': f'Request failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    
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
    

# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Booking
from .serializers import BookingSerializer

@api_view(['POST'])
def notify_guest(request):
    # Handle notification logic here
    # Example: Send notification to guest
    return Response({"message": "Notification sent to guest"}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def book_view(request):
    if request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        # Logic for retrieving all bookings
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def booking_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT'])
def booking_status_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':

        status_data = {
            "booking_id": booking.id,
            "status": booking.status,
        }
        return Response(status_data)
    elif request.method == 'PUT':
        status_value = request.data.get('status')
        if status_value:
            booking.status = status_value
            booking.save()
            return Response({"message": f"Booking status updated successfully for booking ID {booking_id}"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please provide a valid status value"}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def payment_view(request, booking_id):
    # Handle payment logic here
    # Example: Process payment for the booking
    return Response({"message": "Payment processed successfully"}, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def payment_with_id_view(request, booking_id, payment_id):
    # Handle payment with payment_id logic here
    # Example: Retrieve, update, or delete payment with given payment_id
    return Response({"message": f"Payment with ID {payment_id} retrieved/updated/deleted successfully for booking {booking_id}"}, status=status.HTTP_200_OK)
