# Generated by Django 4.2.4 on 2023-08-30 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_user_options_remove_user_date_joined_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='birth_year',
        ),
        migrations.RemoveField(
            model_name='user',
            name='public_visibility',
        ),
    ]