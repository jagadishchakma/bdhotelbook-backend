from rest_framework import serializers
from . import models
from accounts.models import User,Profile,RoomBooked

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.District
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelImage
        fields = '__all__'

class AdvantageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelAdvantage
        fields = '__all__'

#complex serializer relationships
class HotelNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotels
        fields = '__all__'
class RoomSerializer(serializers.ModelSerializer):
    room_image = ImageSerializer(many=True, read_only=True)
    hotel = HotelNestedSerializer(many=True, read_only=True)
    class Meta:
        model = models.HotelRoom
        fields = '__all__'

class RoomNestedSerializer(serializers.ModelSerializer):
    room_image = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = models.HotelRoom
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField(many=False)
    images = ImageSerializer(many=True, read_only=True)
    advantage = AdvantageSerializer(many=True, read_only=True)
    rooms = RoomNestedSerializer(many=True, read_only=True)
    class Meta:
        model = models.Hotels
        fields = '__all__'
    

    def get_district(self, obj):
        return obj.district.slug  

#complex serializer enable for features
#room booked serializer
class RoomBookedSerializer(serializers.ModelSerializer):
    room = RoomSerializer(many=True, read_only=True)
    class Meta:
        model = RoomBooked
        fields = '__all__'
#user profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    room_booked = RoomBookedSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
#user lists serializer
class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = '__all__'


class HotelReviewSerializer(serializers.ModelSerializer):
    user = UserListSerializer(many=False, read_only=True)
    class Meta:
        model = models.HotelReview
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
       