# Generated by Django 5.0.3 on 2024-03-26 11:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytabs', '0003_alter_tab_notes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('securityQuestion1', models.CharField(max_length=100)),
                ('securityAnswer1', models.CharField(max_length=100)),
                ('securityQuestion2', models.CharField(max_length=100)),
                ('securityAnswer2', models.CharField(max_length=100)),
                ('securityQuestion3', models.CharField(max_length=100)),
                ('securityAnswer3', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
