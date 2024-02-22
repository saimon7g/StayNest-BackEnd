from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from authService.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import serializers

import json
def hello_view(request):
    result ={
        
        'message': 'Hello, World from APIGateWay Handler hello_view()',
    }
    return JsonResponse(result)

def HomeData(request):
    result ={
        
        
        'message': 'Hello, World from APIGateWay Handler HomeData()',
    }
    return JsonResponse(result)


import requests
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

@method_decorator(csrf_exempt, name='dispatch')

class RedirectHostView(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, path):
        return self.handle_redirect(request, path)

    def post(self, request, path):
        return self.handle_redirect(request, path)
    
    def put(self, request, path):
        return self.handle_redirect(request, path)

    def handle_redirect(self, request, path):
        auth_token = request.session.get('auth_token', None)
        headers = {'Authorization': f'Token {auth_token}'} if auth_token else {}
        headers['Content-Type'] = 'application/json'
        target_url = f'http://localhost:8080/{path}/'

        try:
            data = request.data
            response = requests.request(request.method, target_url, headers=request.headers, json=data)

            if response.status_code // 100 == 2:
                host = response.data.get('host', {})
                if host:
                    try:
                        user = User.objects.get(id=host.get('host_id'))
                        serializer = UserSerializer(user)
                        if serializer.is_valid():
                            response.data['host'] = serializer.data
                        else:
                            print(serializer.errors)
                    except User.DoesNotExist:
                        print('no host..')

                        
                    except serializers.ValidationError:
                        pass  # Handle serializer validation errors
                return Response(response.json(), status=response.status_code)
            else:
                return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({'error': f'Request failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class RedirectGuestView(APIView):
    def dispatch(self, request, *args, **kwargs):
        # Pass the request to the appropriate method based on the HTTP method used
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, path):
        return self.handle_redirect(request, path)

    def post(self, request, path):

        return self.handle_redirect(request, path)
    def put(self, request, path):
        return self.handle_redirect(request, path)

    # Add other methods as needed

    def handle_redirect(self, request, path):
        # Construct the target URL by appending the original path to http://localhost:8080/
        auth_token = request.session.get('auth_token', None)

        if auth_token is not None:
            # Use the token in subsequent requests
            headers = {'Authorization': f'Token {auth_token}'}
           
        else:
            headers = {}
        headers['Content-Type']='application/json'
        target_url = f'http://localhost:8090/{path}/'

        try:
            # Make a request with custom headers
            print('Request---data---',request.data)
            # response = requests.request(request.method, target_url, headers=headers, data=request.data)
            # data = json.dumps(request.data)
            data=request.data
            # print('req header',request.headers)
            response = requests.request(request.method, target_url, headers=request.headers, json=data)

            # Check if the request was successful (status code 2xx)
            if response.status_code // 100 == 2:
                print('Response---',response.json())
                return Response(response.json(), status=response.status_code)
            else:
                # Handle non-successful response
                return Response(response.json(), status=response.status_code)
            
        except requests.RequestException as e:
            # Handle request exception
            return Response({'error': f'Request failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
