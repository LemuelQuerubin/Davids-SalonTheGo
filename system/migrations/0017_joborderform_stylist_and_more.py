# Generated by Django 4.0.6 on 2022-07-25 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0016_alter_joborderform_appointmentinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='joborderform',
            name='stylist',
            field=models.CharField(max_length=30, null=True, verbose_name='Stylist'),
        ),
        migrations.AlterField(
            model_name='joborderform',
            name='appointmentInfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='system.appointment', verbose_name='Appointment'),
        ),
        migrations.AlterField(
            model_name='joborderform',
            name='totalPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Total'),
        ),
    ]
