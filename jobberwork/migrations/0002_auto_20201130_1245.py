# Generated by Django 3.0.8 on 2020-11-30 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobberwork', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newtask',
            name='location',
            field=models.TextField(),
        ),
    ]