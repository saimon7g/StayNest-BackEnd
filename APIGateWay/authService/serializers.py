from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'phone', 'address', 'profile_picture', 'nid_document', 'passport_document']

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
