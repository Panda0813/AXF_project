# Generated by Django 2.0.5 on 2018-05-21 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_remove_topmenu_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='topmenu',
            name='position',
            field=models.IntegerField(default=1),
        ),
    ]