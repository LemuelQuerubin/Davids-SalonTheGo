# Generated by Django 4.0.6 on 2022-07-13 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_stafftype_rename_gender_admin_gendertype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customertype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customertype', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='gendertype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.gender', verbose_name='Gender'),
        ),
        migrations.AddField(
            model_name='staff',
            name='gendertype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.gender', verbose_name='Gender'),
        ),
        migrations.AddField(
            model_name='staff',
            name='stafftype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.stafftype', verbose_name='Staff Type'),
        ),
        migrations.AlterField(
            model_name='admin',
            name='stafftype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.stafftype', verbose_name='Staff Type'),
        ),
        migrations.AddField(
            model_name='customer',
            name='customertype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.customertype', verbose_name='Customer Type'),
        ),
    ]
