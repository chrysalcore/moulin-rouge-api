from django.contrib import admin
from user_app.models import UserManager, User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'email', 'phone_number']
    search_fields = ['username', 'email']
    ordering = ('name', 'username')

admin.site.register(User, UserAdmin)