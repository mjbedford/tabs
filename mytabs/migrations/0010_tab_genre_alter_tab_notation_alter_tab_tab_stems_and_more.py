# Generated by Django 5.0.3 on 2024-03-27 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytabs', '0009_alter_userprofile_genre1_alter_userprofile_genre2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tab',
            name='genre',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='tab',
            name='notation',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='tab',
            name='tab_stems',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='tab',
            name='tablature',
            field=models.CharField(max_length=5),
        ),
    ]
