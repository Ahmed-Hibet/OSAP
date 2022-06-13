from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Occupation,
    EducationLevel,
    Roll,
    User,
)
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Occupation)
admin.site.register(EducationLevel)
admin.site.register(Roll)