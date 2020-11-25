# Generated by Django 3.0.8 on 2020-11-25 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobberwork', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newtask',
            name='Time',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='newtask',
            name='location',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userpending',
            name='pending',
            field=models.BooleanField(default=False),
        ),
    ]
