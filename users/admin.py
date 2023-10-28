from django.contrib import admin

from users.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'is_staff', 'is_superuser',)
