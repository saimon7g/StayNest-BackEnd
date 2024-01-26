# serializers.py
from rest_framework import serializers
from .models import (
    Location, SomeBasics, PropertyRegistration, RegularAmenity, StandoutAmenity,
    Photo, PropertyRegistrationStep2, Step3, Step4, MealOption, Step5, Step6, Step7, FinalRegistration
)

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'selected_location']

class SomeBasicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SomeBasics
        fields = ['number_of_guests', 'number_of_bedrooms', 'number_of_beds', 'number_of_bathrooms']

class RegularAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularAmenity
        fields = ['name']

class StandoutAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StandoutAmenity
        fields = ['name']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['url', 'description']

class PropertyRegistrationStep2Serializer(serializers.ModelSerializer):
    regular_amenities = RegularAmenitySerializer(many=True)
    standout_amenities = StandoutAmenitySerializer(many=True)
    photos = PhotoSerializer(many=True)

    class Meta:
        model = PropertyRegistrationStep2
        fields = ['registration_id', 'regular_amenities', 'standout_amenities', 'photos']

class Step3Serializer(serializers.ModelSerializer):
    class Meta:
        model = Step3
        fields = ['registration_id', 'house_title', 'highlights', 'description']

class Step4Serializer(serializers.ModelSerializer):
    class Meta:
        model = Step4
        fields = ['registration_id', 'negotiation_availability', 'price', 'discounts', 'security_features']

class MealOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealOption
        fields = ['name', 'description', 'price', 'photo']

class Step5Serializer(serializers.ModelSerializer):
    breakfast_options = MealOptionSerializer(many=True, read_only=True, source='breakfast')
    lunch_options = MealOptionSerializer(many=True, read_only=True, source='lunch')
    dinner_options = MealOptionSerializer(many=True, read_only=True, source='dinner')

    class Meta:
        model = Step5
        fields = ['registration_id', 'breakfast_options', 'lunch_options', 'dinner_options']

class Step6Serializer(serializers.ModelSerializer):
    class Meta:
        model = Step6
        fields = ['registration_id', 'paying_guest']

class Step7Serializer(serializers.ModelSerializer):
    class Meta:
        model = Step7
        fields = ['registration_id', 'selected_dates']

class FinalRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalRegistration
        fields = ['registration_id', 'step1', 'step2', 'step3', 'step4', 'step5', 'step6', 'step7']
