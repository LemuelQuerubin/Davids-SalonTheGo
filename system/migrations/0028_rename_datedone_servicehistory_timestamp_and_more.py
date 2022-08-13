# Generated by Django 4.0.6 on 2022-08-10 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0027_alter_servicehistory_servicename'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicehistory',
            old_name='dateDone',
            new_name='timestamp',
        ),
        migrations.RemoveField(
            model_name='servicehistory',
            name='customerName',
        ),
        migrations.RemoveField(
            model_name='servicehistory',
            name='serviceName',
        ),
        migrations.RemoveField(
            model_name='servicehistory',
            name='serviceType',
        ),
        migrations.AddField(
            model_name='servicehistory',
            name='appointmentInfo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='system.appointment', verbose_name='Appointment'),
        ),
        migrations.AddField(
            model_name='servicehistory',
            name='servicePrices',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='servicehistory',
            name='totalPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, null=True, verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='servicehistory',
            name='finalStylist',
            field=models.CharField(max_length=30, null=True, verbose_name='Stylist'),
        ),
    ]