# Generated by Django 4.0.6 on 2022-07-25 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_alter_appointment_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='contact_num',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='Contact Number'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='services',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
