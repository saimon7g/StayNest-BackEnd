from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .serializers import TemporaryBookingSerializer
from .models import TemporaryBooking
from rest_framework.authtoken.models import Token
from rest_framework import status


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


class NegotiationAsGuestView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, guest_id):
        guest_id = getUserByToken(request)
        # retrieve all Temporarybookings where the guest_id == TemporaryBooking.guest_id
        #Temporary Booking table is the negotiation table

        # Your logic to retrieve negotiation data
        negotiations=TemporaryBooking.objects.filter(guest_id=guest_id)
        serializer = TemporaryBookingSerializer(negotiations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class NegotiationAsHostView(APIView):
    
        # permission_classes = [permissions.IsAuthenticated]
    
        def get(self, request):
            host_id = getUserByToken(request)
            # retrieve all Temporarybookings where the host_id == TemporaryBooking.host_id
            #Temporary Booking table is the negotiation table
    
            # Your logic to retrieve negotiation data
            negotiations=TemporaryBooking.objects.filter(host_id=host_id)
            serializer = TemporaryBookingSerializer(negotiations, many=True)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateStatusView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def put(self, request, negotiation_id):
       
        print(request.data)
        nego_status = request.data['status']
        instance = TemporaryBooking.objects.get(id=negotiation_id)
        if instance:
            instance.status = nego_status
            instance.save()
            return Response({"message":"success"}, status=status.HTTP_200_OK)
        else:
            print("else")
            return Response(status=status.HTTP_400_BAD_REQUEST)
       
class HostProposedView(APIView):
    def put(self,request,negotiation_id):
       
        instance = TemporaryBooking.objects.get(id=negotiation_id)
        if instance:
            instance.negotiation_status = "Host Proposed"
            instance.host_price = request.data['host_price']    

            instance.save()
            return Response({"message":"success"}, status=status.HTTP_200_OK)
        else:
            
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

           

    


       
        
        
        
class NegotiationListView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Your logic to retrieve negotiation data
        print("NegotiationListView")
        print(request)
        # "data": {
        #     "negotiations": [
        #         {
        #             "negotiation_id": "<negotiation id>",
        #             "property_name": "Property Name 1",
        #             "booking_type": "Stay",
        #             "negotiation_status": "pending",
        #             "photo": "base64 encoded image"// photo of propertyy
        #         },
        #         {
        #             "negotiation_id": "<negotiation id>",
        #             "property_name": "Property Name 2",
        #             "booking_type": "Stay with Meals",
        #             "negotiation_status": "accepted",
        #             "photo": "base64 encoded image"
        #         },
        #         {
        #             "negotiation_id": "<negotiation id>",
        #             "property_name": "Property Name 3",
        #             "booking_type": "Paying Guest",
        #             "negotiation_status": "rejected",
        #             "photo": "base64 encoded image"
        #         }
        #     ]
        # }
        
        data = {
            "negotiations": [
                {
                    "negotiation_id": "1",
                    "property_name": "saimon hotel",
                    "booking_type": "Stay",
                    "negotiation_status": "pending",
                    "photo": "base64 encoded image"
                },
                {
                    "negotiation_id": "2",
                    "property_name": "muntasir hotel",
                    "booking_type": "Stay with Meals",
                    "negotiation_status": "accepted",
                    "photo": "base64 encoded image"
                },
                {
                    "negotiation_id": "3",
                    "property_name": "sanim hotel",
                    "booking_type": "Paying Guest",
                    "negotiation_status": "rejected",
                    "photo": "base64 encoded image"
                }
            ]
        }
        return Response(data)
    
        
class NegotiationDetailsView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, negotiation_id):
        # Your logic to retrieve negotiation details
        print("NegotiationDetailsView")
        print(request)
        print(negotiation_id)
        # "data": {
        #     "host": {
        #         "host_id": 123456,
        #         "host_name": "John Doe",
        #         "host_email": "sjbgnfsdjksdjkg@gmail.com",
        #         "host_phone": "1234567890",
        #     },
        #     "propert_details": {
        #         "property_id": 123456,
        #         "property_name": "Aloha",
        #         "property_type": "Villa",
        #         "property_sub_type": "Entire Villa",
        #         "image_data": "sfgsgsdgdfsgsdgsdg",
        #         "address": "123, Aloha Street, Aloha, Aloha",
        #         "number_of_guests": 4,
        #         "number_of_bedrooms": 2,
        #         "number_of_beds": 3,
        #         "number_of_bathrooms": 2,
        #     },
        #     "booking_details": {
        #         "booking_type": "Stay with Meals",
        #         "start_date": "2024-01-12",
        #         "end_date": "2024-01-15",
        #         "staying_price": 300,
        #     },
        #     "meals": {
        #         "breakfast": [
        #             { "name": "Continental", "quantity": 2, "date": "2024-01-12", "price": 10 },
        #             { "name": "Full English", "quantity": 2, "date": "2024-01-12", "price": 10 },
        #         ],
        #         "lunch": [
        #             { "name": "Italian", "quantity": 2, "date": "2024-01-13", "price": 10 },
        #             { "name": "BBQ", "quantity": 2, "date": "2024-01-13", "price": 10 }
        #         ],
        #         "dinner": [
        #             { "name": "Italian", "quantity": 2, "date": "2024-01-13", "price": 10 },
        #             { "name": "BBQ", "quantity": 2, "date": "2024-01-13", "price": 10 }
        #         ]
        #     },
        #     "negotiation_details": {
        #         "negotiation_id": "<negotiation id>",
        #         "default_price": 300,
        #         "guest_price": 250,
        #         "host_price": 200,
        #         "negotiation_status": "offeredbyhost"
        #     }
        # }
        
        data = {
            "host": {
                "host_id": 123456,
                "host_name": "AH Entiaz",
                "host_email": "sjfmgsfjksdfjkg@gmail.com",
                "host_phone": "1234567890",
            },
            "propert_details": {
                "property_id": 123456,
                "property_name": "Aloha",
                "property_type": "Villa",
                "property_sub_type": "Entire Villa",
                "image_data": "sfgsgsdgdfsgsdgsdg",
                "address": "123, Aloha Street, Aloha, Aloha",
                "number_of_guests": 4,
                "number_of_bedrooms": 2,
                "number_of_beds": 3,
                "number_of_bathrooms": 2,
            },
            "booking_details": {
                "booking_type": "Stay with Meals",
                "start_date": "2024-01-12",
                "end_date": "2024-01-15",
                "staying_price": 300,
            },
            "meals": {
                "breakfast": [
                    { "name": "Continental", "quantity": 2, "date": "2024-01-12", "price": 10 },
                    { "name": "Full English", "quantity": 2, "date": "2024-01-12", "price": 10 },
                ],
                "lunch": [
                    { "name": "Italian", "quantity": 2, "date": "2024-01-13", "price": 10 },
                    { "name": "BBQ", "quantity": 2, "date": "2024-01-13", "price": 10 }
                ],
                "dinner": [
                    { "name": "Italian", "quantity": 2, "date": "2024-01-13", "price": 10 },
                    { "name": "BBQ", "quantity": 2, "date": "2024-01-13", "price": 10 }
                ]
            },
            "negotiation_details": {
                "negotiation_id": "1",
                "default_price": 300,
                "guest_price": 250,
                "host_price": 200,
                "negotiation_status": "offeredbyhost"
            }
        }
        return Response(data)
    
class OfferAcceptedByGuestView(APIView):
    # permission_classes = [IsAuthenticated]
    
    # const data = {
    #         negotiation_id: negotiationId,
    #         negotiation_status: "acceptedbyguest",
    #     };

    def put(self, request):
        print("OfferAcceptedByGuestView")
        print(request)
        data = {
            "negotiation_id": "1",
            "negotiation_status": "acceptedbyguest",
        }
        return Response(data)
class OfferRejectedByGuestView(APIView):
    # permission_classes = [IsAuthenticated]
    
    # const data = {
    #         negotiation_id: negotiationId,
    #         negotiation_status: "rejectedbyguest",
    #     };

    def put(self, request):
        print("OfferRejectedByGuestView")
        print(request)
        data = {
            "negotiation_id": "1",
            "negotiation_status": "rejectedbyguest",
        }
        return Response(data)
    
class OfferAcceptedByHostView(APIView):
    # permission_classes = [IsAuthenticated]
    
    # const data = {
    #         negotiation_id: negotiationId,
    #         negotiation_status: "acceptedbyhost",
    #     };

    def put(self, request):
        print("OfferAcceptedByHostView")
        print(request)
        data = {
            "negotiation_id": "1",
            "negotiation_status": "acceptedbyhost",
        }
        return Response(data)
    
class OfferRejectedByHostView(APIView):
    # permission_classes = [IsAuthenticated]
    
    # const data = {
    #         negotiation_id: negotiationId,
    #         negotiation_status: "rejectedbyhost",
    #     };

    def put(self, request):
        print("OfferRejectedByHostView")
        print(request)
        data = {
            "negotiation_id": "1",
            "negotiation_status": "rejectedbyhost",
        }
        return Response(data)
    
class StartNegotiationByGuestView(APIView):
    # permission_classes = [IsAuthenticated]
    
    # const data = {
    #         negotiation_id: negotiationId,
    #         negotiation_status: "pending",
    #     };

    def post(self, request, *args, **kwargs):
        
        print ("StartNegotiationByGuestView")
        print (request.data)
        serializer = TemporaryBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print (" elseeeeeee ------------")
            print (serializer.errors)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    