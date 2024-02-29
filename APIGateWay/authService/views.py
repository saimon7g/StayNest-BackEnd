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


def get_user_id_from_token(request):
    auth_header = request.headers.get('Authorization')
    token_key = auth_header.split(' ')[1]
    token = Token.objects.get(key=token_key)
    user_id = token.user.id
    return user_id

class SignupView(APIView):
    def post(self, request):        
        serializer = UserSerializer(data=request.data)
   
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
#    find auth token from header
    try:

        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header and auth_header.startswith('Token '):
                # Extract the token from the Authorization header
            token_key = auth_header.split(' ')[1]

            try:
                    # Retrieve the Token object using the token key
                token = Token.objects.get(key=token_key)

                    # Delete the token
                token.delete()
            except:
                pass
    except:

        pass

    return Response({"message":"logout done"})
    

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
           


      
class UserView(APIView):
    def get(self, request):
        try:
           
           
            user_id = get_user_id_from_token(request)
            user = User.objects.get(id=user_id)
            serializer = UserProfileSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        