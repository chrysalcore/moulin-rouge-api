from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, name, email, phone_number, password):
        if not email:
            raise ValueError('You must have an email')
        if not username:
            raise ValueError('You must have a username')
        if not password:
            raise ValueError('You must have a password')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            name = name,
            phone_number = phone_number
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, name, email, phone_number, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            name = name,
            password = password,
            phone_number = phone_number
        )
        
        user.is_superadmin = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, default=None)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'phone_number']
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, object=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True