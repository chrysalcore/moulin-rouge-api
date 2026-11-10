from user_app.api.serializers import RegisterSerializer
from user_app.models import User
from rest_framework import response, status, exceptions, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django import contrib, conf
from django.core.mail import send_mail
from django.core.cache import cache
from random import randint

VERIFICATION_CODE_TTL = 600


def verification_cache_key(email):
    return f'verification_code:{email}'

# Method to send verification emails for the user
@api_view(['POST'])
def email_validation_view(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.data.get('username')).exists():
            return response.Response({'warning': 'This username is already in use'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=request.data.get('email')).exists():
            return response.Response({'warning': 'This email is already in use'}, status=status.HTTP_400_BAD_REQUEST)
        
        verification_code = randint(100000, 999999)
        cache.set(verification_cache_key(request.data.get('email')), verification_code, VERIFICATION_CODE_TTL)

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
            cache_key = verification_cache_key(serializer.validated_data['email'])
            if serializer.validated_data['verification_code'] != cache.get(cache_key):
                return response.Response({'status':'The verification code was incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            cache.delete(cache_key)

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
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Function view for user logout
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    if request.method == 'POST':
        refresh = request.data.get('refresh')
        if not refresh:
            return response.Response({'error': 'The refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(refresh).blacklist()
        except TokenError:
            return response.Response({'error': 'Invalid or expired refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(status=status.HTTP_200_OK)

# Function view for user login
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
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
            return response.Response({'error':'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)