# Generated by Django 2.0.5 on 2018-05-22 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_foodtypes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodtypes',
            name='childtypenames',
            field=models.CharField(max_length=150),
        ),
    ]
