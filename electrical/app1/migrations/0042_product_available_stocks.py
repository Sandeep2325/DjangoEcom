# Generated by Django 4.0.2 on 2022-05-21 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0041_banner_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available_stocks',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]