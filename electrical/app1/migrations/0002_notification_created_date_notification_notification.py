# Generated by Django 4.0.2 on 2022-03-30 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date'),
        ),
        migrations.AddField(
            model_name='notification',
            name='notification',
            field=models.TextField(blank=True, null=True),
        ),
    ]
