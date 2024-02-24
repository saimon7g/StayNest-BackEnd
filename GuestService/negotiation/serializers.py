from rest_framework import serializers
from .models import TemporaryBooking, TemporaryMeal



# class MealSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Meal
#         fields = '__all__'

# class BookingSerializer(serializers.ModelSerializer):
#     breakfast = MealSerializer(many=True,required = False)
#     lunch = MealSerializer(many=True,required = False)
#     dinner = MealSerializer(many=True,required = False)

#     class Meta:
#         model = Booking
#         fields = '__all__'

#     def create(self, validated_data):
#         breakfast_data = validated_data.pop('breakfast', [])
#         lunch_data = validated_data.pop('lunch', [])
#         dinner_data = validated_data.pop('dinner', [])

#         booking_instance = Booking.objects.create(**validated_data)

#         self.create_meals(booking_instance, 'breakfast', breakfast_data)
#         self.create_meals(booking_instance, 'lunch', lunch_data)
#         self.create_meals(booking_instance, 'dinner', dinner_data)

#         return booking_instance

#     def create_meals(self, booking_instance, meal_type, meals_data):
#         for meal_data in meals_data:
#             meal = Meal.objects.create(**meal_data)
#             getattr(booking_instance, meal_type).add(meal)

#     def update(self, instance, validated_data):
#         breakfast_data = validated_data.pop('breakfast', [])
#         lunch_data = validated_data.pop('lunch', [])
#         dinner_data = validated_data.pop('dinner', [])

#         instance = super().update(instance, validated_data)

#         self.update_meals(instance, 'breakfast', breakfast_data)
#         self.update_meals(instance, 'lunch', lunch_data)
#         self.update_meals(instance, 'dinner', dinner_data)

#         return instance

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryMeal   
        fields = '__all__'
        
class TemporaryBookingSerializer(serializers.ModelSerializer):
    breakfast = MealSerializer(many=True,required = False)
    lunch = MealSerializer(many=True,required = False)
    dinner = MealSerializer(many=True,required = False)

    class Meta:
        model = TemporaryBooking
        fields = '__all__'

    def create(self, validated_data):
        breakfast_data = validated_data.pop('breakfast', [])
        lunch_data = validated_data.pop('lunch', [])
        dinner_data = validated_data.pop('dinner', [])

        booking_instance = TemporaryBooking.objects.create(**validated_data)

        self.create_meals(booking_instance, 'breakfast', breakfast_data)
        self.create_meals(booking_instance, 'lunch', lunch_data)
        self.create_meals(booking_instance, 'dinner', dinner_data)

        return booking_instance

    def create_meals(self, booking_instance, meal_type, meals_data):
        for meal_data in meals_data:
            meal = TemporaryMeal.objects.create(**meal_data)
            getattr(booking_instance, meal_type).add(meal)

    def update(self, instance, validated_data):
        breakfast_data = validated_data.pop('breakfast', [])
        lunch_data = validated_data.pop('lunch', [])
        dinner_data = validated_data.pop('dinner', [])

        instance = super().update(instance, validated_data)

        self.update_meals(instance, 'breakfast', breakfast_data)
        self.update_meals(instance, 'lunch', lunch_data)
        self.update_meals(instance, 'dinner', dinner_data)

        return instance

    def update_meals(self, booking_instance, meal_type, meals_data):
        getattr(booking_instance, meal_type).clear()
        for meal_data in meals_data:
            meal = TemporaryMeal.objects.create(**meal_data)
            getattr(booking_instance, meal_type).add(meal)


   