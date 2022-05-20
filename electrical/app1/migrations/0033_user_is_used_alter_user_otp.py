# Generated by Django 4.0.2 on 2022-04-11 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0032_user_is_confirmed_alter_user_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp',
            field=models.IntegerField(default=False),
        ),
    ]