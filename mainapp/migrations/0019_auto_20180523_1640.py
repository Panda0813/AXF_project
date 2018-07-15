# Generated by Django 2.0.5 on 2018-05-23 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='imgpath',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.BooleanField(default=True, verbose_name='用户状态'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterModelTable(
            name='user',
            table='axf_user',
        ),
    ]