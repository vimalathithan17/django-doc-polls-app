# Generated by Django 4.2.3 on 2023-07-17 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_registration', '0002_alter_personaldetails_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldetails',
            name='age',
            field=models.IntegerField(default=18),
        ),
    ]
