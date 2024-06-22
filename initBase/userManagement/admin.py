from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import MyUser, walletModel, otpVerificationModel, AccessTokenModel, JwtAuthToken, RefreshTokenModel

from django.contrib.contenttypes.models import ContentType

class CustomUserAdmin(UserAdmin):
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MyUser
    list_display = ("mobile_number",  "is_active", "is_staff", "is_superuser", "date_joined")
    list_filter = ("_active",)
    fieldsets = (
        (None, {"fields": ("mobile_country_code","mobile_number", "password", "pin")}),
        ("Personal info", {"fields": ["date_joined", ]}),
        ("Backend Workers", {"fields": ["OtpField"]}),
        ("Permissions", {"fields": ("_staff", "_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "mobile_country_code",  "pin", "mobile_number", "password1", "password2", "_staff",
                "_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("mobile_number",)
    ordering = ("-id",)


admin.site.register(MyUser, CustomUserAdmin)

admin.site.register(walletModel)
admin.site.register(otpVerificationModel)
admin.site.register(ContentType)
admin.site.register(JwtAuthToken)
admin.site.register(AccessTokenModel)
admin.site.register(RefreshTokenModel)