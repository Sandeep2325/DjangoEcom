# Generated by Django 4.0.2 on 2022-03-04 05:29

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0024_alter_blog_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='url',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
    ]
