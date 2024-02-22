from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    profile_picture =models.TextField(blank=True, null=True)
    nid_document = models.FileField(upload_to='documents/', null=True, blank=True)
    passport_document = models.FileField(upload_to='documents/', null=True, blank=True)
    superhost = models.BooleanField(default=False)

    def __str__(self):
         return self.user.username