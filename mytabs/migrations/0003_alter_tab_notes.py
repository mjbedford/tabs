# Generated by Django 5.0.3 on 2024-03-24 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytabs', '0002_tab_notelist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tab',
            name='notes',
            field=models.CharField(max_length=15000),
        ),
    ]
