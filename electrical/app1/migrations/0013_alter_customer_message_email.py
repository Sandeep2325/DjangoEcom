# Generated by Django 4.0.2 on 2022-03-01 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_alter_customer_message_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_message',
            name='Email',
            field=models.EmailField(max_length=50, null=True),
        ),
    ]