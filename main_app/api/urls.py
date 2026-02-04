from django.urls import path
from main_app.api.views import *

urlpatterns = [
    path('', MainListView.as_view(), name='main-list-view'),
    
    path('categorys/post/', CategoryAddView.as_view(), name='category-add-view'),
    path('categorys/', CategoryListView.as_view(), name='category-list-view'),
    path('categorys/<int:id>/', CategoryDetailView.as_view(), name='category-detail-view'),
    
    path('courses/post/', CourseAddView.as_view(), name='course-add-view'),
    path('courses/', CourseListView.as_view(), name='course-list-view'),
    path('courses/<int:id>/', CourseDetailView.as_view(), name='course-detail-view'),
    
    path('courses/<int:id>/comments/post/', CommentAddView.as_view(), name='comment-add-view'),
    path('courses/<int:id>/comments/', CommentListView.as_view(), name='comment-list-view'),
    path('comments/<int:id>/', CommentDetailView.as_view(), name='comment-detail-view'),
    
    path('reservations/post/', ReservationAddView.as_view(), name='reservation-add-view'),
    path('reservations/', ReservationListView.as_view(), name='reservation-list-view'),
    path('reservations/<int:id>/', ReservationDetailView.as_view(), name='reservation-detail-view'),
    
    path('deliverys/post/', DeliveryAddView.as_view(), name='delivery-add-view'),
    path('deliverys/', DeliveryListView.as_view(), name='delivery-list-view'),
    path('deliverys/<int:id>/', DeliveryDetailView.as_view(), name='delivery-detail-view'),
    
    path('events/post/', EventAddView.as_view(), name='event-add-view'),
    path('events/', EventListView.as_view(), name='event-list-view'),
    path('events/<int:id>/', EventDetailView.as_view(), name='event-detail-view'),
]