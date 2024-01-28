# serializers.py
from rest_framework import serializers
from .models import( Location, SomeBasics, RegularAmenities, StandoutAmenities, Photo,
                    PropertyRegistration, PropertyStep2, PropertyStep3, PropertyStep4,
                      MealOption, PropertyStep5, PayingGuest, PropertyStep7,
                      SelectedDate
)
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['id']

class SomeBasicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SomeBasics
        fields = '__all__'
        read_only_fields = ['id']

class PropertyRegistrationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    some_basics = SomeBasicsSerializer()

    class Meta:
        model = PropertyRegistration
        fields = '__all__'
    def create(self, validated_data):
        location_data = validated_data.pop('location')
        some_basics_data = validated_data.pop('some_basics')

        location_instance = Location.objects.create(**location_data)
        some_basics_instance = SomeBasics.objects.create(**some_basics_data)

        property_registration_instance = PropertyRegistration.objects.create(
                location=location_instance,
                some_basics=some_basics_instance,
                **validated_data
            )
        return property_registration_instance

class RegularAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularAmenities
        fields = '__all__'

class StandoutAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandoutAmenities
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class PropertyStep2Serializer(serializers.ModelSerializer):
    regular_amenities = RegularAmenitiesSerializer(many=True)
    standout_amenities = StandoutAmenitiesSerializer(many=True)
    photos = PhotoSerializer(many=True)

    class Meta:
        model = PropertyStep2
        fields = '__all__'
    def create(self, validated_data):
        regular_amenities_data = validated_data.pop('regular_amenities')
        standout_amenities_data = validated_data.pop('standout_amenities')
        photos_data = validated_data.pop('photos')
        
        property_step2_instance = PropertyStep2.objects.create(**validated_data)

        for regular_amenity_data in regular_amenities_data:
            property_step2_instance.regular_amenities.create(**regular_amenity_data)

        for standout_amenity_data in standout_amenities_data:
            property_step2_instance.standout_amenities.create(**standout_amenity_data)

        for photo_data in photos_data:
            property_step2_instance.photos.create(**photo_data)

        return property_step2_instance

class PropertyStep3Serializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyStep3
        fields = '__all__'

class PropertyStep4Serializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyStep4
        fields = '__all__'

class MealOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealOption
        fields = '__all__'

class PropertyStep5Serializer(serializers.ModelSerializer):
    breakfast = MealOptionSerializer(many=True)
    lunch = MealOptionSerializer(many=True)
    dinner = MealOptionSerializer(many=True)

    class Meta:
        model = PropertyStep5
        fields = '__all__'

    def create(self, validated_data):
        breakfast_data = validated_data.pop('breakfast', [])
        lunch_data = validated_data.pop('lunch', [])
        dinner_data = validated_data.pop('dinner', [])

        property_step5_instance = PropertyStep5.objects.create(**validated_data)

        self.create_meal_options(property_step5_instance, 'breakfast', breakfast_data)
        self.create_meal_options(property_step5_instance, 'lunch', lunch_data)
        self.create_meal_options(property_step5_instance, 'dinner', dinner_data)

        return property_step5_instance

    def create_meal_options(self, property_step5_instance, meal_type, options_data):
        for option_data in options_data:
            meal_option = MealOption.objects.create(**option_data)
            getattr(property_step5_instance, meal_type).add(meal_option)


class PayingGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayingGuest
        fields = '__all__'
class SelectedDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedDate
        fields = ["start_date","end_date"]

class PropertyStep7Serializer(serializers.ModelSerializer):
    selected_dates = SelectedDateSerializer(many=True)

    class Meta:
        model = PropertyStep7
        fields = ['registration_id', 'selected_dates']

    def create(self, validated_data):
        selected_dates_data = validated_data.pop('selected_dates')
        property_step7 = PropertyStep7.objects.create(**validated_data)

        for selected_date_data in selected_dates_data:
            selected_date=SelectedDate.objects.create( **selected_date_data)
            getattr(property_step7, 'selected_dates').add(selected_date)

        return property_step7
    

    # serializers.py


class CompleteRegistrationSerializer(serializers.ModelSerializer):
    step2 = serializers.SerializerMethodField()
    step3 = serializers.SerializerMethodField()
    step4 = serializers.SerializerMethodField()
    step5 = serializers.SerializerMethodField()
    paying_guest = serializers.SerializerMethodField()
    step7 = serializers.SerializerMethodField()

    class Meta:
        model = PropertyRegistration
        fields = '__all__'

    def get_step2(self, obj):
        step2_instance = PropertyStep2.objects.get(registration_id=obj.registration_id)
        serializer = PropertyStep2Serializer(step2_instance)
        return serializer.data

    def get_step3(self, obj):
        step3_instance = PropertyStep3.objects.get(registration_id=obj.registration_id)
        serializer = PropertyStep3Serializer(step3_instance)
        return serializer.data

    def get_step4(self, obj):
        step4_instance = PropertyStep4.objects.get(registration_id=obj.registration_id)
        serializer = PropertyStep4Serializer(step4_instance)
        return serializer.data

    def get_step5(self, obj):
        step5_instance = PropertyStep5.objects.get(registration_id=obj.registration_id)
        serializer = PropertyStep5Serializer(step5_instance)
        return serializer.data

    def get_paying_guest(self, obj):
        paying_guest_instance = PayingGuest.objects.get(registration_id=obj.registration_id)
        serializer = PayingGuestSerializer(paying_guest_instance)
        return serializer.data

    def get_step7(self, obj):
        step7_instance = PropertyStep7.objects.get(registration_id=obj.registration_id)
        serializer = PropertyStep7Serializer(step7_instance)
        return serializer.data
