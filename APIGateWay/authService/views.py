from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer, UserProfileSerializer, HostSerializer


# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         user = User.objects.get(username=request.data['username'])
#         user.set_password(request.data['password'])
#         user.save()
#         token = Token.objects.create(user=user)
#         return Response({'token': token.key, 'user': serializer.data})
#     return Response(serializer.errors, status=status.HTTP_200_OK)

class SignupView(APIView):
    def post(self, request):
        # print("request.data",request.data)
        serializer = UserSerializer(data=request.data)
        # print("after serializer",serializer)
        if serializer.is_valid():
            user=serializer.save()
            guest_group = Group.objects.get(name='guest')
            guest_group.user_set.add(user)
            host_group = Group.objects.get(name='host')
            host_group.user_set.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # print("error ------------           ",serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = get_object_or_404(User, username=request.data['username'])
        if user.check_password(request.data['password']):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def logout(request):
    # Delete the authentication token associated with the user
    if 'auth_token' in request.session:
        auth_token = request.session.pop('auth_token', None)
        if auth_token:
            try:
                token = Token.objects.get(key=auth_token)
                token.delete()
            except Token.DoesNotExist:
                pass  # Token not found, but continue with logout

    return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

class HostSignupView(APIView):
    def post(self, request, uid):
        try:
            user = User.objects.get(id=uid)
            host_group = Group.objects.get(name='host')
            host_group.user_set.add(user)
            return Response({'message': 'User added to host group successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class HostProfileView(APIView):
    def get(self, request, uid):
        try:
            user = User.objects.get(id=uid)
            serializer = HostSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class GuestProfileView(APIView):
    def get(self, request, uid):
        try:
            user = User.objects.get(id=uid)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class HostProfileDetailsView(APIView):
    
    
    
    def get(self, request, uid):
        try:
            user = User.objects.get(id=uid)
            serializer = HostSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           