# Generated by Django 4.0.6 on 2022-07-28 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_customuser_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default-prof.jpg', null=True, upload_to=''),
        ),
    ]
