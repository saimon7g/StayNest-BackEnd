# serializers.py
from rest_framework import serializers
from datetime import date
from django.contrib.auth.models import User
from .models import( Location, SomeBasics, RegularAmenities, StandoutAmenities, Photo,
                    PropertyRegistration, PropertyStep2, PropertyStep3, PropertyStep4,
                      MealOption, PropertyStep5, PayingGuest, PropertyStep7,
                      SelectedDate,PropertyReview,
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
    location = LocationSerializer()
    some_basics = SomeBasicsSerializer()
    step2 = serializers.SerializerMethodField()
    step3 = serializers.SerializerMethodField()
    step4 = serializers.SerializerMethodField()
    step5 = serializers.SerializerMethodField()
    paying_guest = serializers.SerializerMethodField()
    step7 = serializers.SerializerMethodField()

    class Meta:
        model = PropertyRegistration
        fields = ['registration_id', 'location', 'some_basics', 'step2', 'step3', 'step4', 'step5', 'paying_guest', 'step7']

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
        try:
            step5_instance = PropertyStep5.objects.get(registration_id=obj.registration_id)
        except PropertyStep5.DoesNotExist:
        # PropertyStep5 instance does not exist, return None or an empty dictionary
            return None  # or return {} if you prefer an empty dictionary

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

#  {
#       "property_id": "123456",
#       "name": "Cozy Apartment in New York",
#       "location_name": "New York",
#       "price_per_night": 150,
#       "availability": {
#         "check_in": "2024-01-12",
#         "check_out": "2024-01-15"
#       },
#       "photo": "base64convertedstring"
#     },
class ConcisePropertySerializer(serializers.ModelSerializer):
     property_id = serializers.CharField(source='registration_id')
     name = serializers.CharField(source='step3.house_title')
     location_name = serializers.CharField(source='location.selected_location')
     price_per_night = serializers.DecimalField(source='step4.price', max_digits=10, decimal_places=2)
     availability = serializers.SerializerMethodField()
     photo = serializers.SerializerMethodField()          

     class Meta:
        model = PropertyRegistration
        fields = ['property_id', 'name', 'location_name', 'price_per_night','availability', 'photo']


     def get_photo(self, obj):
        # Get the first photo object if it exists, otherwise return None
        first_photo = obj.step2.photos.first()
        return first_photo.image_data if first_photo else None
     def get_availability(self, obj):
            
            step7_instance = PropertyStep7.objects.get(registration_id=obj.registration_id)
            intervals = step7_instance.selected_dates.filter(
                start_date__gte=date.today(), status='available',
            ).order_by('start_date')
            
            if intervals.exists():
                interval = intervals.first()
                serializer = SelectedDateSerializer(interval)
                return serializer.data
            else:
                return None
            


#             {
#   "listing_id": "123456",
#   "name": "Cozy Apartment in New York",
#   "location": "New York",
#   "property_type": "Apartment",
#   "property_subtype": "City Center",
#   "description": "A comfortable and stylish apartment in the heart of the city.",
#   "price": 150,
#   "availability": {
#     "check_in": "2024-01-12",
#     "check_out": "2024-01-15"
#   },
#   "regular_amenities": ["Wi-Fi", "Kitchen", "Air Conditioning", "TV"],
#   "standout_amenities": ["Private Balcony", "Jacuzzi"],
#   "highlights": [
#     "Close to public transportation",
#     "Walking distance to popular attractions"
#   ],
#   "host": {
#     "host_id": "789",
#     "host_name": "John Doe",
#     "host_email": "john.doe@example.com"
#   },
#   "photos": [
#     {
#       "url": "https://example.com/photo1.jpg",
#       "title": "Living Room"
#     },
#     {
#       "url": "https://example.com/photo2.jpg",
#       "title": "Bedroom"
#     },
#     {
#       "url": "https://example.com/photo3.jpg",
#       "title": "Kitchen"
#     }
#   ],
#   "reviews": [
#     {
#       "user": "Alice",
#       "comment": "Great location and cozy atmosphere. Loved it!",
#       "rating": 5
#     },
#     {
#       "user": "Bob",
#       "comment": "Clean and well-maintained. Would stay again.",
#       "rating": 4
#     }
#     // Add more review objects as needed
#   ]
# }


class PropertyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyReview
        fields = '__all__'
        
class DetailedPropertySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='step3.house_title')
    location = serializers.CharField(source='location.selected_location')
    some_basics = SomeBasicsSerializer()
    description = serializers.CharField(source='step3.description')
    price = serializers.DecimalField(source='step4.price', max_digits=10, decimal_places=2)
    availability = serializers.SerializerMethodField()
    regular_amenities = serializers.SerializerMethodField()
    standout_amenities = serializers.SerializerMethodField()
    highlights = serializers.JSONField(source='step3.highlights')
    booking_options=serializers.SerializerMethodField()
    host = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = PropertyRegistration
        fields = ['name', 'location','some_basics', 'property_type', 'property_sub_type', 'description', 'price', 'availability', 'regular_amenities', 'standout_amenities', 'highlights', 'booking_options','host', 'photos', 'reviews']
    def get_booking_options(self, obj):
        return {
            "stay": obj.stay,
            "stay_with_meal": obj.stay_with_meal,
            "paying_guest": obj.paying_guest
        }

    def get_availability(self, obj):
        try:
            step7_instance = PropertyStep7.objects.get(registration_id=obj.registration_id)
            intervals = step7_instance.selected_dates.filter(
                start_date__gte=date.today(), status='available',
            ).order_by('start_date')

            if intervals.exists():
                
                serializer = SelectedDateSerializer(intervals, many=True)
                return serializer.data
            else:
                return None
        except PropertyStep7.DoesNotExist:
            return None

    def get_regular_amenities(self, obj):
        try:
            step2_instance = PropertyStep2.objects.get(registration_id=obj.registration_id)
            amenities = step2_instance.regular_amenities.all()
            return [amenity.name for amenity in amenities]
        except PropertyStep2.DoesNotExist:
            return []

    def get_standout_amenities(self, obj):
        try:
            step2_instance = PropertyStep2.objects.get(registration_id=obj.registration_id)
            amenities = step2_instance.standout_amenities.all()
            return [amenity.name for amenity in amenities]
        except PropertyStep2.DoesNotExist:
            return []

    def get_host(self, obj):
            return {
                    "host_id": obj.user.id,
                    "details":"setdetails",
                    }

    def get_photos(self, obj):
        try:
            step2_instance = PropertyStep2.objects.get(registration_id=obj.registration_id)
            photos = step2_instance.photos.all()
            return [
                
                # send a dictionary with the image_data and title
                {
                    "image_data":photo.image_data,
                    "title": photo.description,
                }
                 for photo in photos
            ]
        except PropertyStep2.DoesNotExist:
            return []

    def get_reviews(self, obj):
        try:
            property_id = obj.registration_id
            reviews = PropertyReview.objects.filter(property_id=property_id)
            return [
                {
                    "user": review.user.username,
                    "comment": review.comment,
                    "rating": review.rating
                }
                for review in reviews
            ]
        except PropertyReview.DoesNotExist:
            return []
        
