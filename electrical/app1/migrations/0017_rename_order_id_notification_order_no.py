# Generated by Django 4.0.2 on 2022-03-31 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_alter_notification_order_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='order_id',
            new_name='order_no',
        ),
    ]