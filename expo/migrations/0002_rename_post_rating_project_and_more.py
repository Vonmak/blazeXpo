# Generated by Django 4.0.5 on 2022-06-10 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='post',
            new_name='project',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='content_average',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='design_average',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='score',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='usability_average',
        ),
    ]