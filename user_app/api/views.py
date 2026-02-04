from user_app.api.serializers import RegisterSerializer
from user_app.models import User
from rest_framework import response, status, exceptions
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django import contrib, conf
from django.core.mail import send_mail
from random import randint

verification_code = None

# Method to send verification emails for the user
@api_view(['POST'])
def email_validation_view(request):
    if request.method == 'POST':
        global verification_code
        verification_code = randint(100000, 999999)
        if User.objects.filter(username=request.data.get('username')).exists():
            return response.Response({'warning': 'This username is already in use'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=request.data.get('email')).exists():
            return response.Response({'warning': 'This email is already in use'}, status=status.HTTP_400_BAD_REQUEST)
        
        subject = 'Asunto'
        message = 'Use this code to validate your email address: ' + str(verification_code)
        from_email = conf.settings.EMAIL_HOST_USER
        recipient_list = [request.data.get('email')]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        return response.Response(status=status.HTTP_200_OK)

# Function view for user sign up
@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        
        if serializer.is_valid():
            if serializer.validated_data.get('verification_code') != verification_code:
                response.Response({'status':'The verification code was incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            account = serializer.save()
            data['response'] = 'Register Success'
            data['user'] = account.username
            data['name'] = account.name
            data['email'] = account.email
            data['phone_number'] = account.phone_number
            data['tokens'] = {
                'refresh': str(RefreshToken.for_user(account)),
                'access': str(AccessToken.for_user(account))
            }
            return response.Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Function view for user logout
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return response.Response(status=status.HTTP_200_OK)

# Function view for user login
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        print(request.data)
        data = {}
        email = request.data.get('email')
        password = request.data.get('password')
        
        account = contrib.auth.authenticate(email=email, password=password)
        if account is not None:
            data['response'] = 'Login Success'
            data['user'] = account.username
            data['name'] = account.name
            data['email'] = account.email
            data['phone_number'] = account.phone_number
            data['tokens'] = {
                'refresh': str(RefreshToken.for_user(account)),
                'access': str(AccessToken.for_user(account))
            }
            return response.Response(data, status=status.HTTP_200_OK)
        else:
            return response.Response({'error':'Invalid credentials.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)