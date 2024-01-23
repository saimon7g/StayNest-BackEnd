# models.py
import uuid 
from django.db import models

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    selected_location = models.CharField(max_length=255)

class SomeBasics(models.Model):
    number_of_guests = models.PositiveIntegerField()
    number_of_bedrooms = models.PositiveIntegerField()
    number_of_beds = models.PositiveIntegerField()
    number_of_bathrooms = models.FloatField()

class PropertyRegistration(models.Model):
    registration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step1 = models.OneToOneField(Location, on_delete=models.CASCADE)
    step2 = models.OneToOneField(SomeBasics, on_delete=models.CASCADE, null=True, blank=True)
    # Add other steps as needed

class RegularAmenity(models.Model):
    name = models.CharField(max_length=255)

class StandoutAmenity(models.Model):
    name = models.CharField(max_length=255)

class Photo(models.Model):
    url = models.URLField()
    description = models.CharField(max_length=255)

class PropertyRegistrationStep2(models.Model):
    registration_id = models.OneToOneField(PropertyRegistration, on_delete=models.CASCADE)
    regular_amenities = models.ManyToManyField(RegularAmenity)
    standout_amenities = models.ManyToManyField(StandoutAmenity)
    photos = models.ManyToManyField(Photo)
