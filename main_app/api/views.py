from rest_framework import generics, permissions, exceptions
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Avg, Count
from datetime import timedelta, date
from main_app.api.serializers import CourseSerializer, ReservationSerializer, DeliverySerializer, CommentSerializer, EventSerializer, CategorySerializer
from main_app.api.throttling import CourseThrottle, AddThrottle, ListThrottle, CommentThrottle, DetailThrottle
from main_app.api.pagination import CoursePagination, CommentPagination, InfoPagination
from main_app.api.permissions import IsAuthorOrAdmin, IsMainUser
from main_app.models import Course, Reservation, Delivery, Comment, Event, Category


def update_course_rating(course):
    stats = Comment.objects.filter(course=course).aggregate(average=Avg('rating'), total=Count('id'))
    course.rating = stats['average'] or 0
    course.ratings_count = stats['total']
    course.save(update_fields=['rating', 'ratings_count'])

class MainListView(generics.GenericAPIView):
    pagination_class = CoursePagination
    permission_classes = [permissions.AllowAny]
    throttle_classes = [CourseThrottle]
    
    def get(self, request, *args, **kwargs):
        courses = Course.objects.filter(available=True).order_by('-rating', 'price')[:5]
        all_events = Event.objects.all()
        events = all_events
        # for i in all_events:
        #     if 0 <= abs((i.date_init - date.today())).days <= 30:
        #         events.append(i)
        
        return Response({
            'courses': CourseSerializer(courses, many=True).data,
            'events': EventSerializer(events, many=True).data,
        })

class CategoryAddView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsMainUser]
    throttle_classes = [AddThrottle]
    queryset = Category.objects.all()

class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = InfoPagination
    permission_classes = [IsMainUser]
    throttle_classes = [ListThrottle]
    
    def get_queryset(self):
        return Category.objects.all().order_by('name')

class CategoryDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsMainUser]
    throttle_classes = [DetailThrottle]
    queryset = Category.objects.all()
    lookup_field = 'name'

class CourseAddView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsMainUser]
    throttle_classes = [AddThrottle]
    queryset = Course.objects.all()

class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = CoursePagination
    permission_classes = [permissions.AllowAny]
    throttle_classes = [CourseThrottle]
    
    def get_queryset(self):
        category = self.request.query_params.get('category', 'Pizza')
        return Course.objects.filter(category=category, available=True).order_by('price')

class CourseDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsMainUser]
    throttle_classes = [DetailThrottle]
    queryset = Course.objects.all()
    lookup_field = "id"

class CommentAddView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [CommentThrottle]
    queryset = Comment.objects.all()
    
    def perform_create(self, serializer):
        id = self.kwargs['id']
        course = Course.objects.get(pk=id)
        
        user = self.request.user
        prev_commits = Comment.objects.filter(course=course, user=user)
        
        if prev_commits.exists():
            raise exceptions.ValidationError('This user has previously committed this course.')

        with transaction.atomic():
            serializer.save(course=course, user=user)
            update_course_rating(course)

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ListThrottle]
    
    def get_queryset(self):
        id = self.kwargs['id']
        return Comment.objects.filter(course=id).order_by('-date')
    
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdmin]
    throttle_classes = [CommentThrottle]
    queryset = Comment.objects.all()
    lookup_field = 'id'

    def perform_update(self, serializer):
        with transaction.atomic():
            comment = serializer.save()
            update_course_rating(comment.course)

    def perform_destroy(self, instance):
        course = instance.course
        with transaction.atomic():
            instance.delete()
            update_course_rating(course)

class ReservationAddView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [AddThrottle]
    queryset = Reservation.objects.all()
    
    def perform_create(self, serializer):
        date = serializer.validated_data['date']
        evt = Event.objects.all()
        price = 150
        
        if Reservation.objects.filter(date=date, user=self.request.user).exists():
            raise exceptions.ValidationError('This user already has a reservation for that date')
        for i in evt:
            if i.date_init <= date.date() <= i.date_end:
                price *= (1 - i.discount)
        
        serializer.save(user=self.request.user, price=price)

class ReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    pagination_class = InfoPagination
    permission_classes = [IsAuthorOrAdmin]
    throttle_classes = [ListThrottle]
    
    def get_queryset(self):
        user = self.request.query_params.get('user', self.request.user)
        data = Reservation.objects.filter(user=user).order_by('date')
        return data

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthorOrAdmin]
    throttle_classes = [DetailThrottle]
    queryset = Reservation.objects.all()
    lookup_field = 'id'
    
class DeliveryAddView(generics.CreateAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [AddThrottle]
    queryset = Delivery.objects.all()
    
    def perform_create(self, serializer):
        date = serializer.validated_data['date']
        courses = serializer.validated_data['courses']
        evt = Event.objects.all()
        tp = 0
        
        for i in Delivery.objects.filter(user=self.request.user):  
            if (i.date - timedelta(hours=5)) < date < (i.date + timedelta(hours=5)):
                raise exceptions.ValidationError('That delivery is closed to others')
        for i in courses:
            tp += (Course.objects.get(id=int(i)).price * courses[i])
        for i in evt:
            if i.date_init <= date.date() <= i.date_end:
                tp *= (1 - i.discount)
                tp += 200
        
        serializer.save(user=self.request.user, total_price=tp)

class DeliveryListView(generics.ListAPIView):
    serializer_class = DeliverySerializer
    pagination_class = InfoPagination
    permission_classes = [IsAuthorOrAdmin]
    throttle_classes = [ListThrottle]
    
    def get_queryset(self):
        user = self.request.query_params.get('user', self.request.user)
        data = Delivery.objects.filter(user=user).order_by('date')
        return data

class DeliveryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthorOrAdmin]
    throttle_classes = [DetailThrottle]
    queryset = Delivery.objects.all()
    lookup_field = 'id'

class EventAddView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsMainUser]
    throttle_classes = [AddThrottle]
    queryset = Event.objects.all()
    
    def perform_create(self, serializer):
        date1 = serializer.validated_data['date_init']
        date2 = serializer.validated_data['date_end']
        
        if date1 < date2:
            exceptions.ValidationError('Init\'s date must be less than or equal that end\'s sdate')
        
        serializer.save()
    
class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    pagination_class = InfoPagination
    permission_classes = [IsMainUser]
    throttle_classes = [ListThrottle]
    
    def get_queryset(self):
        return Event.objects.all().order_by('date_init')

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsMainUser]
    throttle_classes = [DetailThrottle]
    queryset = Event.objects.all()
    lookup_field = 'id'