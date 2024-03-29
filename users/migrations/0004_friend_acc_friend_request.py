# Generated by Django 3.0.4 on 2020-10-14 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_auto_20201014_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester_username', models.CharField(max_length=100)),
                ('target_username', models.CharField(max_length=100)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester_r', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_r', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friend_acc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u1_username', models.CharField(max_length=100)),
                ('u2_username', models.CharField(max_length=100)),
                ('u1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester_t', to=settings.AUTH_USER_MODEL)),
                ('u2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_t', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
