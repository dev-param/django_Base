from django.contrib import admin
from .models import CustomUsers, LogsModel
from django.contrib.auth.admin import UserAdmin
# Register your models here.



@admin.register(CustomUsers)
class CustomuserAdmin(UserAdmin):
    fieldsets = [x for x in UserAdmin.fieldsets]
    fieldsets.pop(0)
    fieldsets.insert(0, ((None, {'fields': ('username', 'password', 'mobile_number')})))

    ordering = ("-id",)
   


admin.site.register(LogsModel)
