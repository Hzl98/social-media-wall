# Generated by Django 3.0.4 on 2020-11-22 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0008_auto_20201122_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wall',
            name='logo',
            field=models.CharField(default='', max_length=100),
        ),
    ]