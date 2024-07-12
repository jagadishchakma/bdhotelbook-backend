from django.db import models
from django.contrib.auth.models import User
from hotels.models import HotelRoom

# Create your models here.
class RoomBooked(models.Model):
    room = models.ManyToManyField(HotelRoom)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='accounts/images/', default='accounts/images/default-profile.png')
    address = models.CharField(max_length=200, null=True, blank=True)
    phone_no = models.IntegerField(null=True, blank=True)
    balance = models.IntegerField(default=0.0)
    room_booked = models.ManyToManyField(RoomBooked)
    birth_year = models.IntegerField(null=True, blank=True)
    birth_month = models.IntegerField(null=True, blank=True)
    birth_date = models.IntegerField(null=True, blank=True)
    gender = models.CharField(choices=[('Male', 'Male'),('Female','Female')],max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self) -> str:
        return self.user.username
