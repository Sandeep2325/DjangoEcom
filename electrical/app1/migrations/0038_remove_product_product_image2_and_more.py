# Generated by Django 4.0.2 on 2022-02-18 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0037_remove_product_product_image_product_product_image1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_image2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_image3',
        ),
    ]
