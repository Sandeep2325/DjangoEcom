# Generated by Django 3.2 on 2022-02-09 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20220208_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
