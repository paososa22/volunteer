# Generated by Django 4.2.4 on 2023-09-26 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunidad', '0025_interesados'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interesados',
            name='confirmar',
            field=models.CharField(blank=True, choices=[('Y', 'Si'), ('N', 'No')], max_length=30, null=True),
        ),
    ]
