# Generated by Django 2.1.5 on 2019-01-07 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians', '0002_auto_20190105_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=500, verbose_name='Courte description'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, max_length=60, verbose_name='Nom'),
        ),
    ]