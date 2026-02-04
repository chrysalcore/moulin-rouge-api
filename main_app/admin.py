from django.contrib import admin
from main_app.models import Course, Reservation, Delivery, Category, Comment, Event

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    ordering = ('name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['rating', 'course', 'user', 'date']
    search_fields = ['user', 'course']
    list_filter = ['rating', 'date']
    ordering = ('-date', 'user')
    date_hierarchy = 'date'

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'category', 'available']
    search_fields = ['course',]
    ordering = ('course',)
    list_filter = ['category', 'available', 'rating']

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']
    search_fields = ['user',]
    ordering = ('-date',)
    list_filter = ['date',]
    date_hierarchy = 'date'

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'date']
    search_fields = ['user', 'location']
    ordering = ('-date',)
    list_filter = ['date',]
    date_hierarchy = 'date'

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount', 'date_init', 'date_end']
    search_fields = ['name',]
    ordering = ('-date_init',)
    list_filter = ['date_init', 'date_end']
    date_hierarchy = 'date_init'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Event, EventAdmin)