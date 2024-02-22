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

class Reservation(models.Model):
     STATUS_CHOICES = [
        ('requested', 'requested'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('ready_for_payment', 'Ready for Payment'),
        ('negotiation_going_on', 'Negotiation Going On'),
    ]
     reservation_id = models.AutoField(primary_key=True)
     property_id = models.IntegerField()
     property_name = models.CharField(max_length=100)
     guest_id =  models.IntegerField()
     host_id =  models.IntegerField()
     start_date = models.DateField()
     end_date = models.DateField()
     total_price = models.DecimalField(max_digits=10, decimal_places=2)
     total_meals_price = models.DecimalField(max_digits=10, decimal_places=2)
     total_staying_price = models.DecimalField(max_digits=10, decimal_places=2)
     number_of_persons = models.PositiveIntegerField()
     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

class Booking(models.Model):
    STATUS_CHOICES = [
        ('requested', 'requested'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('ready_for_payment', 'Ready for Payment'),
        ('negotiation_going_on', 'Negotiation Going On'),
    ]
    

class MealOption(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)

class MealBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='meal_bookings')
    meal_type = models.CharField(max_length=10)  # 'breakfast', 'lunch', or 'dinner'
    options = models.ManyToManyField(MealOption,related_name='meal_options')

class Pricing(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='reservation')
    reservation_price = models.DecimalField(max_digits=10, decimal_places=2)
    staying_price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_nights = models.IntegerField()
    number_of_persons = models.IntegerField()
    total_staying_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_meals_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reservation for Booking ID: {self.booking.id}"

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


class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    nid_document = models.FileField(upload_to='documents/', null=True, blank=True)
    passport_document = models.FileField(upload_to='documents/', null=True, blank=True)
    joined_at = models.DateTimeField(default=get_local_time)

    def __str__(self):
        return self.first_name + ' ' + (self.surname if self.surname else '')

    class Meta:
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'

class GuestReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guest_reviews')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='guest_reviews')
    review = models.TextField()
    rating = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.property.name} by {self.user.username}"