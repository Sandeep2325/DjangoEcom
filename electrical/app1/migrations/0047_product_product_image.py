# Generated by Django 4.0.2 on 2022-02-18 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0046_remove_product_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='product', verbose_name='Product Image'),
        ),
    ]
