# Generated by Django 4.0.6 on 2022-07-25 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_alter_appointment_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='customer_fname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Walk-in First Name'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='customer_lname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Walk-in Last Name'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='contact_num',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='Walk-in Contact Number'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, verbose_name='Walk-in Email Address'),
        ),
    ]