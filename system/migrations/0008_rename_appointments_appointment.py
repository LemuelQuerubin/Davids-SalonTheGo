# Generated by Django 4.0.5 on 2022-07-14 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_appointments_firststylist_appointments_secondstylist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Appointments',
            new_name='Appointment',
        ),
    ]