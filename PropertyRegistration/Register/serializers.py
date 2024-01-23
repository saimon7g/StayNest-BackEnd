# serializers.py

from rest_framework import serializers
from .models import Location, SomeBasics, PropertyRegistration, RegularAmenity, StandoutAmenity, Photo, PropertyRegistrationStep2
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'selected_location']

class SomeBasicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SomeBasics
        fields = ['number_of_guests', 'number_of_bedrooms', 'number_of_beds', 'number_of_bathrooms']

class PropertyRegistrationSerializer(serializers.ModelSerializer):
    step1 = LocationSerializer()
    step2 = SomeBasicsSerializer(required=False, allow_null=True)

    class Meta:
        model = PropertyRegistration
        fields = ['registration_id', 'step1', 'step2']

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
    registration_id = PropertyRegistrationSerializer()
    regular_amenities = RegularAmenitySerializer(many=True)
    standout_amenities = StandoutAmenitySerializer(many=True)
    photos = PhotoSerializer(many=True)

    class Meta:
        model = PropertyRegistrationStep2
        fields = ['registration_id', 'regular_amenities', 'standout_amenities', 'photos']
