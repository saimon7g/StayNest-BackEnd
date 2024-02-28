# models.py
from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta

def get_local_time():
    return timezone.localtime(timezone.now())

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    selected_location = models.CharField(max_length=255)

class SomeBasics(models.Model):
    number_of_guests = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    number_of_beds = models.IntegerField()
    number_of_bathrooms = models.FloatField()

class PropertyRegistration(models.Model):
    STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('completed', 'Completed'),
    ]

    registration_id = models.BigAutoField(primary_key=True)
    property_type = models.CharField(max_length=255)
    online_type=models.CharField(max_length=255,default='Standard')
    property_sub_type = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='Location')
    some_basics = models.ForeignKey(SomeBasics, on_delete=models.CASCADE,related_name='SomeBasics')
    
    stay=models.BooleanField(default=True)
    stay_with_meal=models.BooleanField(default=True)
    paying_guest=models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #created_at= localtime 
    created_at = models.DateTimeField(default=get_local_time)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='incomplete')
    def delete(self, *args, **kwargs):
        # Delete related location and some_basics
        self.location.delete()
        self.some_basics.delete()
        # Call superclass delete method to delete the PropertyRegistration instance
        super(PropertyRegistration, self).delete(*args, **kwargs)
    def mark_as_completed(self):
        # Check if PropertyStep2 exists for this registration ID
        try:
            PropertyStep2.objects.get(registration_id=self.registration_id)
        except ObjectDoesNotExist:
            # PropertyStep2 does not exist, so return an error
            return {"error": "PropertyStep2 not found for this registration ID"}

        # Check if PropertyStep3 exists for this registration ID
        try:
            PropertyStep3.objects.get(registration_id=self.registration_id)
        except ObjectDoesNotExist:
            # PropertyStep3 does not exist, so return an error
            return {"error": "PropertyStep3 not found for this registration ID"}
        # Check if PropertyStep4 exists for this registration ID
        try:
            PropertyStep4.objects.get(registration_id=self.registration_id)
        except ObjectDoesNotExist:
            # PropertyStep4 does not exist, so return an error
            return {"error": "PropertyStep4 not found for this registration ID"}
        # Check if PropertyStep7 exists for this registration ID
        try:
            PropertyStep7.objects.get(registration_id=self.registration_id)
        except ObjectDoesNotExist:
            # PropertyStep7 does not exist, so return an error
            return {"error": "PropertyStep7 not found for this registration ID"}
        self.status = 'completed'
        self.save()
        return {"message": "Property registration marked as completed"}
        
class RegularAmenities(models.Model):
    name = models.CharField(max_length=255)

class StandoutAmenities(models.Model):
    name = models.CharField(max_length=255)


class Photo(models.Model):
    description = models.TextField()
    image_data = models.TextField(blank=True, null=True) 
    
class PropertyStep2(models.Model):
    registration_id = models.OneToOneField(PropertyRegistration, on_delete=models.CASCADE, related_name='step2')
    regular_amenities = models.ManyToManyField(RegularAmenities)
    standout_amenities = models.ManyToManyField(StandoutAmenities)
    photos = models.ManyToManyField(Photo)
    def delete(self, *args, **kwargs):
        # Delete related regular_amenities
        self.regular_amenities.clear()

        # Delete related standout_amenities
        self.standout_amenities.clear()

        # Delete related photos
        self.photos.clear()

        # Call superclass delete method to delete the PropertyStep2 instance
        super(PropertyStep2, self).delete(*args, **kwargs)

class PropertyStep3(models.Model):
    registration_id = models.OneToOneField(PropertyRegistration, on_delete=models.CASCADE, related_name='step3')
    house_title = models.CharField(max_length=255)
    highlights = models.JSONField()
    description = models.TextField()

class PropertyStep4(models.Model):
    registration_id = models.OneToOneField(PropertyRegistration, on_delete=models.CASCADE, related_name='step4')
    negotiation_availability = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounts = models.JSONField()
    security_features = models.JSONField()

class MealOption(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.TextField()

class PropertyStep5(models.Model):
    registration_id = models.OneToOneField(PropertyRegistration, on_delete=models.CASCADE, related_name='step5')
    breakfast = models.ManyToManyField(MealOption, related_name='breakfast_options')
    lunch = models.ManyToManyField(MealOption, related_name='lunch_options')
    dinner = models.ManyToManyField(MealOption, related_name='dinner_options')
    def delete(self, *args, **kwargs):
        # Clear related breakfast, lunch, and dinner options
        self.breakfast.clear()
        self.lunch.clear()
        self.dinner.clear()

        # Call superclass delete method to delete the PropertyStep5 instance
        super(PropertyStep5, self).delete(*args, **kwargs)

class PayingGuest(models.Model):  # Step 6
    registration_id = models.OneToOneField(PropertyRegistration, on_delete=models.CASCADE, related_name='paying_guest_detail')
    description = models.TextField()
    meal_price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.TextField()

class SelectedDate(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'unavailable'),
    ]
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')


class PropertyStep7(models.Model):
    registration_id = models.OneToOneField(PropertyRegistration, on_delete=models.CASCADE, related_name='step7')
    selected_dates =  models.ManyToManyField(SelectedDate, related_name='selected_dates')
    def delete(self, *args, **kwargs):
        # Clear related selected dates
        self.selected_dates.clear()

        # Call superclass delete method to delete the PropertyStep7 instance
        super(PropertyStep7, self).delete(*args, **kwargs)
    



class PropertyReview(models.Model):
    property_id = models.ForeignKey(PropertyRegistration, on_delete=models.CASCADE)
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewer_name=models.TextField()
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(default=get_local_time)

