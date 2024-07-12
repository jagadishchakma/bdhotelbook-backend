from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile,RoomBooked
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from hotels.serializers import RoomSerializer,HotelReviewSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError


# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

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
    review = HotelReviewSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'

#user registration serializer
class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']

    def save(self):
        #retrive user form data
        username = self.validated_data['username']
        email = self.validated_data['email']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        #validation userform
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error':'Username already exists!'})
        if password != confirm_password:
            raise serializers.ValidationError({'error':'Password does not match!'})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error':'Email already exists!'})
        
        
        #save userform
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.is_active = False
        user.set_password(password)
        user.save()

        #save userprofile
        Profile.objects.create(user=user)

        #email verification setup
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f"http://127.0.0.1:8000/account/active/{uid}/{token}"
        mail_subject = "Please verify your email"
        mail_body = render_to_string('mail_confirm.html', {'confirm_link':confirm_link})
        send_mail = EmailMultiAlternatives(mail_subject,'',to=[user.email])
        send_mail.attach_alternative(mail_body, 'text/html')
        send_mail.send()


#user login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

#user balance update serialize
class BalanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['balance']


#user passwrod change serializer
class PasswordChangeSerializer(serializers.Serializer):
    old_pass = serializers.CharField(required=True)
    new_pass = serializers.CharField(required=True)

    def validate_old_pass(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError("Old password does not match.")
        return value

    def validate_new_pass(self, value):
        validate_password(value)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_pass'])
        user.save()

#profile image change serializer
class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']