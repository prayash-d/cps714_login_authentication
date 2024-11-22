# Generated by Django 5.1.3 on 2024-11-21 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Customer', 'Customer'), ('Retailer', 'Retailer'), ('Partner', 'Partner'), ('Admin', 'Admin')], max_length=10, verbose_name='Role'),
        ),
    ]
