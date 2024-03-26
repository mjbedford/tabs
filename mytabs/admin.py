from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Tab, UserProfile



class UserProfileInLine(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "userprofile"

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInLine]

# Register your models here.
admin.site.register(Tab)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
