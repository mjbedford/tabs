# Generated by Django 5.0.3 on 2024-03-22 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytabs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tab',
            name='notelist',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]