# Generated by Django 4.2.4 on 2023-09-26 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comunidad', '0030_interesados_deleted_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interesados',
            name='deleted_date',
        ),
    ]
