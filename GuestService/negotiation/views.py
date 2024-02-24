from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .serializers import TemporaryBookingSerializer

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
        
        
    