# Generated by Django 4.2.3 on 2023-07-19 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_registration', '0003_alter_personaldetails_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldetails',
            name='profile_image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
