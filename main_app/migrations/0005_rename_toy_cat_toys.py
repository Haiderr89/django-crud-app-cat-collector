# Generated by Django 5.1.7 on 2025-03-18 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_cat_toy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cat',
            old_name='toy',
            new_name='toys',
        ),
    ]
