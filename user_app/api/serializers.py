from rest_framework import serializers
from user_app.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'name', 'email',  'phone_number', 'password', 'password_confirmation']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        password = self.validated_data['password']
        password_confirmation = self.validated_data['password_confirmation']
        
        if password != password_confirmation:
            raise serializers.ValidationError({'error': 'The password and it\'s confirmation are not equals.'})
        
        account = User.objects.create_user(
            email=self.validated_data['email'], 
            username=self.validated_data['username'],
            name=self.validated_data['name'],
            password=self.validated_data['password'],
            phone_number=self.validated_data['phone_number']
        )
        account.save()
        return account