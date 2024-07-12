from django.db import models
from django.contrib.auth.models import User


class District(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='hotels/districtImages/')

    def __str__(self) -> str:
        return self.name


class HotelImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='hotels/hotelImages/')
    def __str__(self) -> str:
        return self.name

class HotelAdvantage(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class HotelRoom(models.Model):
    room_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)
    room_sq = models.CharField(max_length=100)
    room_television = models.BooleanField(default=False)
    room_wifi = models.BooleanField(default=True)
    room_bed = models.CharField(max_length=100)
    room_price = models.IntegerField()
    room_view = models.CharField(max_length=100)
    room_image = models.ManyToManyField(HotelImage)
    room_booked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.room_name



class Hotels(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='hotels')
    address = models.CharField(max_length=300)
    description = models.TextField()
    images = models.ManyToManyField(HotelImage)
    advantage = models.ManyToManyField(HotelAdvantage)
    rooms = models.ManyToManyField(HotelRoom, related_name='hotel')
    distance = models.TextField(max_length=200, null=True, blank=True)
    

    def __str__(self) -> str:
        return self.name
    
    class Meta: 
        verbose_name_plural = 'Hotels'

class HotelReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(default=1)
    comment = models.TextField(default='Good')
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE, related_name='hotel_review')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"{str(self.rating)}";