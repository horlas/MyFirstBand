# Generated by Django 2.1.5 on 2019-01-07 16:16

from django.db import migrations
import djangoyearlessdate.models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians', '0003_auto_20190107_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth_year',
            field=djangoyearlessdate.models.YearField(blank=True, null=True, verbose_name='Année de naissance'),
        ),
    ]