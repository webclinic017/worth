# Generated by Django 4.1.3 on 2023-01-10 01:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_rename_total_ppmresult_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ppmresult',
            name='dt',
            field=models.DateTimeField(default=django.utils.timezone.now, unique=True),
        ),
    ]
