# Generated by Django 4.0 on 2024-10-12 12:37

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
