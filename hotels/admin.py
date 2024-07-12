from django.contrib import admin
from . import models


# Register district models
@admin.register(models.District)
class MyModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id','name', 'slug', 'image']


# Register hotel image models
@admin.register(models.HotelImage)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','image']

# Register hotel advantage models
@admin.register(models.HotelAdvantage)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','icon']

# Register hotel rooms models
@admin.register(models.HotelRoom)
class MyModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('room_name',)}
    list_display = ['id','room_name']

# Register hotels models
@admin.register(models.Hotels)
class MyModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id','name']

# Register hotels review model
@admin.register(models.HotelReview)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['id','rating', 'user', 'comment', 'created_at']