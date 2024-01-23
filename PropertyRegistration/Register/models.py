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

class Step3(models.Model):
    registration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house_title = models.CharField(max_length=255)
    highlights = models.JSONField()
    description = models.TextField()

class Step4(models.Model):
    registration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negotiation_availability = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounts = models.JSONField()
    security_features = models.JSONField()

class MealOption(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.URLField()

class Step5(models.Model):
    registration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    breakfast = models.ManyToManyField(MealOption, related_name='breakfast_options')
    lunch = models.ManyToManyField(MealOption, related_name='lunch_options')
    dinner = models.ManyToManyField(MealOption, related_name='dinner_options')

class Step6(models.Model):
    registration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paying_guest = models.JSONField()

class Step7(models.Model):
    registration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    selected_dates = models.JSONField()

class FinalRegistration(models.Model):
    registration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step1 = models.OneToOneField(Location, on_delete=models.CASCADE)
    step2 = models.OneToOneField(SomeBasics, on_delete=models.CASCADE, null=True, blank=True)
    step3 = models.OneToOneField(Step3, on_delete=models.CASCADE, null=True, blank=True)
    step4 = models.OneToOneField(Step4, on_delete=models.CASCADE, null=True, blank=True)
    step5 = models.OneToOneField(Step5, on_delete=models.CASCADE, null=True, blank=True)
    step6 = models.OneToOneField(Step6, on_delete=models.CASCADE, null=True, blank=True)
    step7 = models.OneToOneField(Step7, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.registration_id)
