# Generated by Django 4.2.4 on 2023-08-26 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunidad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=500)),
                ('organization_mail', models.EmailField(max_length=300)),
                ('organization_phone', models.PositiveIntegerField()),
                ('organization_dir', models.CharField(max_length=800)),
                ('organization_web', models.URLField(max_length=400)),
                ('organization_desc', models.CharField(max_length=1000)),
            ],
        ),
    ]
