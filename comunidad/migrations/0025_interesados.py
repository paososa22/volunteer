# Generated by Django 4.2.4 on 2023-09-26 01:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comunidad', '0024_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interesados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_interes', models.DateTimeField(auto_now_add=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('confirmar', models.CharField(choices=[('Y', 'Si'), ('N', 'No')], max_length=30)),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comunidad.organization1')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
