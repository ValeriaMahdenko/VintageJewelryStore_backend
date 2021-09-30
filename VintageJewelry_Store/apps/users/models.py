from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from VintageJewelry_Store.apps.validation import validate_name
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from VintageJewelry_Store.apps.users.manager import ShopUserManager


# Create your models here.
class ShopUser(AbstractBaseUser):
    class Meta:
        verbose_name = "User"

    first_name = models.CharField(max_length=60, validators=[validate_name])
    last_name = models.CharField(max_length=60, validators=[validate_name])
    email = models.EmailField(max_length=180, unique=True)
    country = CountryField(blank=True, blank_label='(Select country)')
    city = models.CharField(max_length=60, blank=True,
        validators=[validate_name])
    street = models.CharField(max_length=60, blank=True)
    phone = PhoneNumberField(blank=True)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = ShopUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_active

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
