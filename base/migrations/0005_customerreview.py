# Generated by Django 4.0.6 on 2022-08-11 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_customuser_profile_pic'),
        ('base', '0004_measurementtype_otcproduct_measurement_num_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(max_length=280, null=True, verbose_name='Review')),
                ('admin_reply', models.TextField(blank=True, max_length=300, null=True, verbose_name='Admin Reply')),
                ('is_like', models.BooleanField(null=True, verbose_name='Like')),
                ('is_dislike', models.BooleanField(null=True, verbose_name='Dislike')),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.customer')),
                ('orderpickup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.orderpickup')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.otcproduct')),
            ],
        ),
    ]
