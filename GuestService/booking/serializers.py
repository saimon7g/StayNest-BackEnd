from rest_framework import serializers
from .models import Property, MealOption, MealBooking, Pricing
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class MealOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealOption
        fields = ['name', 'price','quantity']

class MealBookingSerializer(serializers.ModelSerializer):
    options = MealOptionSerializer(many=True)

    class Meta:
        model = MealBooking
        fields = ['selected', 'options']

class PricingSerializer(serializers.ModelSerializer):
    meals = serializers.SerializerMethodField()

    class Meta:
        model = Pricing
        fields = ['reservation_price', 'staying_price_per_night', 'number_of_nights', 'number_of_persons', 'total_staying_price', 'meals', 'total_meals_price']

    def get_meals(self, obj):
        meal_bookings = obj.booking.meal_bookings.all()
        meal_serializer = MealBookingSerializer(meal_bookings, many=True)
        return meal_serializer.data

class BookingSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=20)
    message = serializers.CharField()
    reservation_id = serializers.CharField()
    check_in_date = serializers.DateField()
    check_out_date = serializers.DateField()
    pricing = PricingSerializer()
    property = serializers.CharField()
    user = serializers.CharField()
    booking_issue_date = serializers.DateTimeField()
    confirmation_date = serializers.DateTimeField()
    class Meta:
        fields = ['status', 'message', 'reservation_id', 'check_in_date', 'check_out_date', 'pricing', 'property', 'user', 'booking_issue_date', 'confirmation_date']
