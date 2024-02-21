from django.db import models
from django.contrib.auth.models import User

class TemporaryBooking(models.Model):
    booking_id = models.BigAutoField(primary_key=True)
    property_id = models.BigIntegerField()
    guest_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temporary_bookings_as_guest')
    host_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temporary_bookings_as_host')
    booking_type = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'temporary_booking'
        verbose_name = 'Temporary Booking'
        verbose_name_plural = 'Temporary Bookings'

class Negotiation(models.Model):
    negotiation_id = models.BigAutoField(primary_key=True)
    booking_id = models.ForeignKey(TemporaryBooking, on_delete=models.CASCADE, related_name='negotiations')
    default_price= models.DecimalField(max_digits=10, decimal_places=2)
    guest_price = models.DecimalField(max_digits=10, decimal_places=2)
    host_price = models.DecimalField(max_digits=10, decimal_places=2)
    negotiation_status = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'negotiation'
        verbose_name = 'Negotiation'
        verbose_name_plural = 'Negotiations'

class TemporaryMeal(models.Model):
    meal_id = models.BigAutoField(primary_key=True)
    booking = models.ForeignKey(TemporaryBooking, on_delete=models.CASCADE, related_name='meals')
    meal_type = models.CharField(max_length=255)
    meal_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'temporary_meal'
        verbose_name = 'Temporary Meal'
        verbose_name_plural = 'Temporary Meals'
