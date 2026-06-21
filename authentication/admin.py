from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LoginHistory

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'full_name', 'role', 'college', 'is_verified', 'is_staff']
    list_filter = ['role', 'is_verified', 'is_staff', 'is_superuser', 'created_at']
    fieldsets = UserAdmin.fieldsets + (
        ('Brainora Profile Info', {
            'fields': (
                'full_name', 'profile_picture', 'bio', 
                'college', 'university', 'branch', 'semester', 
                'college_id', 'phone_contact', 'gender', 
                'location', 'date_of_birth', 'role', 'is_verified', 
                'two_factor_enabled'
            )
        }),
        ('OTP & Lockout Security', {
            'fields': ('otp', 'otp_expiry', 'failed_login_attempts', 'lockout_until')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Brainora Profile Info', {
            'fields': ('full_name', 'email', 'role', 'college', 'is_verified')
        }),
    )
    search_fields = ['username', 'email', 'full_name', 'college']
    ordering = ['username']
    readonly_fields = ['created_at', 'updated_at']

class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip_address', 'login_time', 'user_agent']
    list_filter = ['login_time']
    search_fields = ['user__username', 'user__email', 'ip_address']
    readonly_fields = ['login_time']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(LoginHistory, LoginHistoryAdmin)
