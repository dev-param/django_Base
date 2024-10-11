from django.contrib import admin
from .models import (
                        CustomUsers,
                        LogsModel,
                        PendingTaskModel,
                        AuthTokenModel,
                        TokenModel,
                        XAuth,
                        XAuthSetup
                        
                    ) 
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(CustomUsers)
class CustomuserAdmin(UserAdmin):
    fieldsets = [x for x in UserAdmin.fieldsets]
    fieldsets.pop(0)
    fieldsets.insert(0, ((None, {'fields': ('username', 'password', 'mobile_number')})))
    fieldsets.pop(2)
    fieldsets.insert(2, (('Permissions', {'fields': ('_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')})))
    fieldsets.append((('Other', {'fields': list(['jwtSessions'])})))

    # remove is_active from filter data in admin panel we work on this later
    list_filter = [filter for filter in UserAdmin.list_filter if filter != 'is_active']

    ordering = ("-id",)
   


admin.site.register(LogsModel)
admin.site.register(PendingTaskModel)
admin.site.register(AuthTokenModel)
admin.site.register(TokenModel)
# class MembershipInline(admin.TabularInline):
#     model = XAuth
#     extra = 1

# class XAuthSetupAdmin(admin.ModelAdmin):
#     inlines = (MembershipInline,)

admin.site.register(XAuthSetup)
admin.site.register(XAuth)