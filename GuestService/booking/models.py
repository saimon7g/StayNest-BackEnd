from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta

def get_local_time():
    return timezone.localtime(timezone.now())
# Create your models here.
class GuestNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guest_notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for guest {self.user.username}: {self.message}"
def validate_host_user(user):
    if not user.groups.filter(name='host').exists():
        raise ValidationError('This user is not in the "host" group.')


class Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    meal_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    property_id = models.BigIntegerField()
    property_name = models.CharField(max_length=255,default='ABC Home')
    property_photo = models.TextField(null=True)
    guest_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_guest')
    host_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_host')
    booking_type = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_guests = models.IntegerField()
    breakfast = models.ManyToManyField(Meal, related_name='breakfast_options', blank=True)
    lunch = models.ManyToManyField(Meal, related_name='lunch_options', blank=True)
    dinner = models.ManyToManyField(Meal, related_name='dinner_options', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=get_local_time)
    updated_at = models.DateTimeField(default=get_local_time)
   
        



class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payment ID: {self.id}, User: {self.user.username}, Booking ID: {self.booking_id}"
    
    class Meta:
        managed = False
        db_table = 'payment'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'





