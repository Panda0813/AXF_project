# Generated by Django 2.0.5 on 2018-05-21 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_swipermenu'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('trackid', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('img', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=50)),
                ('position', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_shop',
            },
        ),
    ]