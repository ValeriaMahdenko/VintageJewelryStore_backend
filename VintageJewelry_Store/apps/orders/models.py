from django.db import models
from VintageJewelry_Store.apps.validation import validate_price
from VintageJewelry_Store import settings
from VintageJewelry_Store.apps.products.models import Product


# Create your models here.
class OrderProducts(models.Model):
    class Meta:
        db_table = 'order_products'
    amount_selected = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)


class Order(models.Model):
    class Meta:
        ordering = ['-status', 'total_price']

    LST_STATUS = (
        ('Completed', 'Completed'),
        ('Opened', 'Opened')
    )
    status = models.CharField(max_length=50, choices=LST_STATUS,
        default='Opened')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    selected_products = models.ManyToManyField(Product, through=OrderProducts)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,
        validators=[validate_price], null=True)
