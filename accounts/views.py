from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . import serializers
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import IsAuthenticated

#user list
class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer

#user registration
class RegisterView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Registration successful! please verify your email for activate  acccount', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#user email verification
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token) and user.is_active==False:
        user.is_active = True
        user.save()
        return HttpResponseRedirect('http://localhost:5173/account/login?status=success')
    elif user is not None and default_token_generator.check_token(user,token) and user.is_active==True:
        return HttpResponseRedirect('http://localhost:5173/account/login?status=already_verified')
    return HttpResponseRedirect('http://localhost:5173/account/login?status=failure')

#user login
class LoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({'token':token.key, 'user_id':user.id})
            else:
                return Response({'error':'Invalid Credential'})
        return Response(serializer.errors)

#user logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            print(request.user)
            request.user.auth_token.delete()
            return Response({'success':'logout'})
        except Exception as e:
            return Response({'error':'logout failed'})

#user balance update
class BalanceUpdateView(UpdateAPIView):
    serializer_class = serializers.BalanceUpdateSerializer
    permission_classes = [IsAuthenticated]


    def put(self, request, *args, **kwargs):
        profile = self.request.user.profile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        balance = serializer.validated_data['balance']
        profile.balance += balance
        profile.save(
            update_fields = ['balance']
        )

        return Response({'balance': profile.balance}, status=status.HTTP_200_OK)

#password change view
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Password changed successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#image profile upload
class ProfileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = serializers.ProfileImageSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile image updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#profile personal info update
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = serializers.ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile personal information updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#user basic info update
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        print(request.data)
        serializer = serializers.UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User personal information updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)