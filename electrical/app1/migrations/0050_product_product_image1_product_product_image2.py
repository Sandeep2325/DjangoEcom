# Generated by Django 4.0.2 on 2022-02-18 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0049_product_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image1',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='product', verbose_name='Product Image 1'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image2',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='product', verbose_name='Product Image 2'),
        ),
    ]
