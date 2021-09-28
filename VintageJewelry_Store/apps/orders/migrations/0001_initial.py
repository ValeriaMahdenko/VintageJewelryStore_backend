# Generated by Django 3.1.7 on 2021-09-28 19:40

import VintageJewelry_Store.apps.validation
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('Opened', 'Opened')], default='Opened', max_length=50)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[VintageJewelry_Store.apps.validation.validate_price])),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('selected_products', models.ManyToManyField(to='products.Product')),
            ],
            options={
                'ordering': ['-status', 'total_price'],
            },
        ),
    ]