# Generated by Django 5.1.1 on 2024-11-10 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]