# Generated by Django 3.0.4 on 2020-11-22 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0006_auto_20201114_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='wall',
            name='wall',
            field=models.ImageField(blank=True, upload_to='walls'),
        ),
    ]
