from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from jalali_date import datetime2jalali


# Register your models here.

@admin.register(models.User)
class UserAdmin(UserAdmin):
    list_display = ['phone', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_customer',
                    'is_seller']
    list_filter = ['is_active', 'is_blocked', 'is_staff', 'is_superuser', 'is_customer', 'is_seller']
    search_fields = ['phone', 'email', 'first_name', 'last_name']
    empty_value_display = '-empty-'
    ordering = ['-date_joined']  # error username darim
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات فردی', {'fields': ('first_name', 'last_name', 'email')}),
        (
            'دسترسی‌ها',
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_blocked', 'is_customer', 'is_seller', 'groups',
                        'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('get_last_login_jalali', 'get_created_jalali')}),
    )
    # فیلدهای زیر فقط خواندنی باشند تا در فرم ادمین خطا ندهند
    readonly_fields = ['get_last_login_jalali', 'get_created_jalali']

    @admin.display(description='تاریخ عضویت', ordering='date_joined')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%a, %d %b %Y %H:%M:%S')

    @admin.display(description='تاریخ آخرین لاگین', ordering='last_login')
    def get_last_login_jalali(self, obj):
        return datetime2jalali(obj.last_login).strftime('%a, %d %b %Y %H:%M:%S')


@admin.register(models.OTPRequest)
class OTPRequestAdmin(admin.ModelAdmin):
    list_display = ['phone', 'otp_code', 'get_created_jalali', 'wrong_attempts', 'is_used']
    list_filter = ['wrong_attempts', 'is_used']
    list_editable = ['is_used']
    search_fields = ['phone']

    @admin.display(description='زمان ارسال', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a, %d %b %Y %H:%M:%S')
