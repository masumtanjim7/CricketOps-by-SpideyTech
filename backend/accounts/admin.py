from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'status', 'locale', 'is_staff', 'date_joined')
    search_fields = ('phone', 'email')