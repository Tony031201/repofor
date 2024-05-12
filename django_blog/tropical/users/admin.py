from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfile)


class AdminCode1(admin.ModelAdmin):
    list_display = ['email','is_used']
    search_fields = ['email']

    class Meta:
        model=code_1

admin.site.register(code_1,AdminCode1)

class AdminCode2(admin.ModelAdmin):
    list_display = ['email','is_used']
    search_fields = ['email']

    class Meta:
        model=code_2

admin.site.register(code_2,AdminCode2)