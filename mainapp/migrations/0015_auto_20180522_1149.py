# Generated by Django 2.0.5 on 2018-05-22 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_auto_20180522_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodtypes',
            name='id',
        ),
        migrations.AlterField(
            model_name='foodtypes',
            name='typeid',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
