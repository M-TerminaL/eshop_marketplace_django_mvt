from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.

# Create User Manager for User Model
class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('وارد کردن شماره تلفن همراه الزامیست.')

        if 'email' in extra_fields and extra_fields['email']:
            extra_fields['email'] = self.normalize_email(extra_fields['email'])

        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        if not password:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('وارد کردن شماره تلفن همراه الزامیست.')
        if not password:
            raise ValueError('وارد کردن رمز عبور الزامیست.')

        # create superuser
        # password is required
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('سوپریوزر حتماً باید دارای ویژگی is_staff=True باشد.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('سوپریوزر حتماً باید دارای ویژگی is_superuser=True باشد.')

        user = self.create_user(phone, password, **extra_fields)
        return user




# Create Custom User Model with AbstractUser
class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, db_index=True, verbose_name='شماره تلفن همراه')
    username = None
    password = models.CharField(max_length=120, null=True, blank=True, verbose_name='گذرواژه')
    first_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='نام خانوادگی')
    email = models.EmailField(max_length=30, null=True, blank=True, db_index=True, unique=True, verbose_name='ایمیل')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ عضویت')
    last_login = models.DateTimeField(auto_now=True, verbose_name='آخرین لاگین')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_staff = models.BooleanField(default=False, verbose_name='کارمند')
    is_superuser = models.BooleanField(default=False, verbose_name='ابرکابر / مدیرفروشگاه')
    is_customer = models.BooleanField(default=True, verbose_name='مشتری')
    is_seller = models.BooleanField(default=False, verbose_name='فروشنده')
    is_blocked = models.BooleanField(default=False, verbose_name='بلاک شده / نشده')

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELD = []

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        return self.phone