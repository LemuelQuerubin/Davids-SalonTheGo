# Generated by Django 4.0.6 on 2022-07-25 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0015_joborderform_serviceprices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joborderform',
            name='appointmentInfo',
            field=models.OneToOneField(default=66, on_delete=django.db.models.deletion.PROTECT, to='system.appointment'),
            preserve_default=False,
        ),
    ]
