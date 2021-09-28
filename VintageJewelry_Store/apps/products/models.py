from django.db import models
from VintageJewelry_Store.apps.validation import (
    validate_name, validate_price
)
from VintageJewelry_Store import settings


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50, validators=[validate_name])
    brand_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2,
        validators=[validate_price])
    description = models.TextField(blank=True)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    material = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(null=True, blank=True)
