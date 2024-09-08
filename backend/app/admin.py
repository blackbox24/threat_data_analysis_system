from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(Threat)
admin.site.register(SystemHealth)
admin.site.register(Incident)
admin.site.register(IncidentReport)
admin.site.register(CustomUser, CustomUserAdmin)
