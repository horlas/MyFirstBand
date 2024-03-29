# Generated by Django 2.1.7 on 2019-03-17 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0006_auto_20190317_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicianannouncement',
            name='code',
            field=models.CharField(blank=True, max_length=5, verbose_name='code postal'),
        ),
        migrations.AlterField(
            model_name='musicianannouncement',
            name='county_name',
            field=models.CharField(blank=True, max_length=60, verbose_name='Nom du département'),
        ),
        migrations.AlterField(
            model_name='musicianannouncement',
            name='town',
            field=models.CharField(blank=True, max_length=60, verbose_name='Ville'),
        ),
    ]
