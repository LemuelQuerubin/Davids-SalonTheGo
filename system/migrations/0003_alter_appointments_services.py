# Generated by Django 4.0.5 on 2022-07-04 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_alter_appointments_appointmentstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='services',
            field=models.JSONField(default=''),
        ),
    ]
