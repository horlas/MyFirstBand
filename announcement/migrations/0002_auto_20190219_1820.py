# Generated by Django 2.1.5 on 2019-02-19 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicianannouncement',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]