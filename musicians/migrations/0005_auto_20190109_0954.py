# Generated by Django 2.1.5 on 2019-01-09 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians', '0004_auto_20190107_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='dept',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='code',
            field=models.CharField(blank=True, max_length=5, verbose_name='code postal'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='county_name',
            field=models.CharField(blank=True, max_length=60, verbose_name='Nom du département'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='town',
            field=models.CharField(blank=True, max_length=60, verbose_name='Ville'),
        ),
    ]
