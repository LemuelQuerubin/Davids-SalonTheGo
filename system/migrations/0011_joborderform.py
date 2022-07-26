# Generated by Django 4.0.6 on 2022-07-25 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_insproduct_totalused'),
        ('system', '0010_appointment_customer_fname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobOrderform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_today', models.DateTimeField(auto_now_add=True)),
                ('servicePrices', models.DecimalField(decimal_places=2, max_digits=9)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('consumed', models.BooleanField(default=False)),
                ('appointmentInfo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.appointment')),
                ('insproductused', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.insproduct')),
            ],
        ),
    ]
