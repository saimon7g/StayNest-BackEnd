from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

class Property(models.Model):
    property_id = models.IntegerField(primary_key=True)  # Property_id explicitly provided
    name = models.CharField(max_length=100) 
    description = models.TextField()
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    num_bedrooms = models.PositiveIntegerField()
    num_bathrooms = models.PositiveIntegerField()
    max_occupancy = models.PositiveIntegerField()
    amenities = models.TextField()  # Store as JSON or CSV string
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', validators=[validate_host_user])
    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('requested', 'requested'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('ready_for_payment', 'Ready for Payment'),
        ('negotiation_going_on', 'Negotiation Going On'),
    ]
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_issue_date = models.DateTimeField(auto_now_add=True)
    confirmation_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Booking ID: {self.id}, Property: {self.property.name}, User: {self.user.username}"


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

