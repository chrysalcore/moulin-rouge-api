from rest_framework import serializers
from main_app.models import Course, Reservation, Delivery, Comment, Event, Category
import datetime, pytz

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ['available']
    
class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'
    
    def get_status(self, obj):
        return obj.date < pytz.UTC.localize(datetime.datetime.now())
    
    def validate_date(self, value):
        if value < pytz.UTC.localize(datetime.datetime.now()):
            raise serializers.ValidationError('That date is wrong')
        if (value - pytz.UTC.localize(datetime.datetime.now())).days < 1:
            raise serializers.ValidationError('That date is nearly')
        if len(Reservation.objects.filter(date=(value + datetime.timedelta(hours=1)))) == 4  or len(Reservation.objects.filter(date=(value - datetime.timedelta(hours=1)))) == 4 or len(Reservation.objects.filter(date=value)) == 4:
            raise serializers.ValidationError('Dont have available tables for that hour')
        return value

class DeliverySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Delivery
        fields = '__all__'
            
    def get_status(self, obj):
        return obj.date < pytz.UTC.localize(datetime.datetime.now())
    
    def validate_date(self, value):
        if value < pytz.UTC.localize(datetime.datetime.now()):
            raise serializers.ValidationError('That date is wrong')
        if (value - pytz.UTC.localize(datetime.datetime.now())).days < 2:
            raise serializers.ValidationError('That date is nearly')
        return value