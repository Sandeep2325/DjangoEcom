# Generated by Django 4.0.2 on 2022-03-08 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_remove_product_rating_average_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating_average',
            field=models.FloatField(default=0),
        ),
    ]
