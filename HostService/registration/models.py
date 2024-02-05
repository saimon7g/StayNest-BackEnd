# models.py
from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    selected_location = models.CharField(max_length=255)

class SomeBasics(models.Model):
    number_of_guests = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    number_of_beds = models.IntegerField()
    number_of_bathrooms = models.FloatField()

from django.db import models

class PropertyRegistration(models.Model):
    registration_id = models.BigAutoField(primary_key=True)
    property_type = models.CharField(max_length=255)
    property_sub_type = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    some_basics = models.ForeignKey(SomeBasics, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    photo = models.URLField()

class PropertyStep5(models.Model):
    registration_id = models.OneToOneField(PropertyRegistration, on_delete=models.CASCADE, related_name='step5')
    breakfast = models.ManyToManyField(MealOption, related_name='breakfast_options')
    lunch = models.ManyToManyField(MealOption, related_name='lunch_options')
    dinner = models.ManyToManyField(MealOption, related_name='dinner_options')

class PayingGuest(models.Model):  # Step 6
    registration_id = models.OneToOneField(PropertyRegistration, on_delete=models.CASCADE, related_name='paying_guest')
    description = models.TextField()
    meal_price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.URLField()

class SelectedDate(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()


class PropertyStep7(models.Model):
    registration_id = models.OneToOneField(PropertyRegistration, on_delete=models.CASCADE, related_name='step7')
    selected_dates =  models.ManyToManyField(SelectedDate, related_name='selected_dates')



