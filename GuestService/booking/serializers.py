from rest_framework import serializers

from .models import Booking, Meal

# class MealOptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MealOption
#         fields = '__all__'

# class PropertyStep5Serializer(serializers.ModelSerializer):
#     breakfast = MealOptionSerializer(many=True)
#     lunch = MealOptionSerializer(many=True)
#     dinner = MealOptionSerializer(many=True)

#     class Meta:
#         model = PropertyStep5
#         fields = '__all__'

#     def create(self, validated_data):
#         breakfast_data = validated_data.pop('breakfast', [])
#         lunch_data = validated_data.pop('lunch', [])
#         dinner_data = validated_data.pop('dinner', [])

#         property_step5_instance = PropertyStep5.objects.create(**validated_data)

#         self.create_meal_options(property_step5_instance, 'breakfast', breakfast_data)
#         self.create_meal_options(property_step5_instance, 'lunch', lunch_data)
#         self.create_meal_options(property_step5_instance, 'dinner', dinner_data)

#         return property_step5_instance

#     def create_meal_options(self, property_step5_instance, meal_type, options_data):
#         for option_data in options_data:
#             meal_option = MealOption.objects.create(**option_data)
#             getattr(property_step5_instance, meal_type).add(meal_option)



class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    breakfast = MealSerializer(many=True)
    lunch = MealSerializer(many=True)
    dinner = MealSerializer(many=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def create(self, validated_data):
        breakfast_data = validated_data.pop('breakfast', [])
        lunch_data = validated_data.pop('lunch', [])
        dinner_data = validated_data.pop('dinner', [])

        booking_instance = Booking.objects.create(**validated_data)

        self.create_meals(booking_instance, 'breakfast', breakfast_data)
        self.create_meals(booking_instance, 'lunch', lunch_data)
        self.create_meals(booking_instance, 'dinner', dinner_data)

        return booking_instance

    def create_meals(self, booking_instance, meal_type, meals_data):
        for meal_data in meals_data:
            meal = Meal.objects.create(**meal_data)
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
    