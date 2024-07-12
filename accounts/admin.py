from django.contrib import admin
from .models import Profile,RoomBooked

# Register your models here.
@admin.register(RoomBooked)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['id']
@admin.register(Profile)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','phone_no', 'balance']