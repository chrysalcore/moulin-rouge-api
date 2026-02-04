from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user_app.models import User

# Models
class Category(models.Model):
    name = models.CharField(max_length=15, unique=True, primary_key=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    course = models.CharField(max_length=50)
    img = models.ImageField(upload_to='images/')
    description = models.TextField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    gramage = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0, editable=False)
    ratings_count = models.IntegerField(default=0, editable=False)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.course + '   ' + str(self.gramage) + 'g   ' + str(self.price) + '$'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=250)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.rating) + ' ' + self.text[:20] + '... '

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    people = models.IntegerField(validators=[MaxValueValidator(4), MinValueValidator(1)])
    date = models.DateTimeField(auto_now_add=False)
    price = models.FloatField(default=0.0, editable=False)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.date)

class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.JSONField(default=dict)
    total_price = models.FloatField(default=0.0, editable=False)
    location = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=False)
    
    def __str__(self):
        return str(self.user) + ' - ' + str(self.date)
    
class Event(models.Model):
    img = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    discount = models.FloatField(default=0.0, validators=[MaxValueValidator(1.0), MinValueValidator(0.0)])
    date_init = models.DateField(auto_now_add=False)
    date_end = models.DateField(auto_now_add=False)
    
    def __str__(self):
        return self.name + ' ' + str(self.date_init) + ' - ' + str(self.date_end)