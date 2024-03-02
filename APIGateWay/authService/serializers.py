from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.CharField(source='profile.profile_picture')
    phone= serializers.CharField(source='profile.phone')
    address = serializers.CharField(source='profile.address')
    class Meta:
        model = User
        fields = ['id', 'username','phone', 'address', 'profile_picture']



class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)  # Extract profile data
        user = User.objects.create_user(**validated_data)  # Create user object
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)  # Create associated profile
        return user
# "host": {
#             "host_id": "789",
#             "name": "Rafi",
#             "email": "john.doe@example.com",
#             "response_rate": "100%",
#             "response_time": "within an hour",
#             "super_host": true,
#             "profile_pic":

# class HostSerializer(serializers.Serializer):
#     host_id = serializers.CharField()
#     name = serializers.CharField()
#     email = serializers.EmailField()
#     response_rate = serializers.CharField()
#     response_time = serializers.CharField()
#     super_host = serializers.BooleanField()
#     profile_pic = serializers.CharField()


class HostSerializer(serializers.Serializer):
    host_id = serializers.IntegerField(source='id')
    name = serializers.CharField(source='username')
    response_rate = serializers.SerializerMethodField()
    response_time = serializers.SerializerMethodField()
    super_host = serializers.BooleanField(source='profile.superhost')
    profile_pic = serializers.CharField(source='profile.profile_picture')
    phone = serializers.CharField(source='profile.phone')
    class Meta:
        model = User
        fields = ['host_id', 'name', 'email', 'response_rate', 'response_time', 'super_host', 'profile_pic', 'email', 'phone']

    def get_response_rate(self, obj):
        return "100%"
    
    def get_response_time(self, obj):
        return "within an hour"
    

