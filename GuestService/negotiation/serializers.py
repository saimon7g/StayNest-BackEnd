from rest_framework import serializers
from .models import TemporaryBooking, Negotiation, TemporaryMeal

class TemporaryBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryBooking
        fields = ['booking_id', 'property_id', 'guest_id', 'host_id', 'booking_type', 'start_date', 'end_date']
        read_only_fields = ['booking_id']  # Making booking_id read-only as it's a primary key

class NegotiationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negotiation
        fields = ['negotiation_id', 'booking_id', 'default_price', 'guest_price', 'host_price', 'negotiation_status']
        read_only_fields = ['negotiation_id']  # Making negotiation_id read-only as it's a primary key

class TemporaryMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryMeal
        fields = ['meal_id', 'booking', 'meal_type', 'meal_name', 'quantity', 'date', 'price']
        read_only_fields = ['meal_id']  # Making meal_id read-only as it's a primary key
