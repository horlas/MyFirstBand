# Generated by Django 2.1.5 on 2019-02-14 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians', '0011_auto_20190214_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=60, unique=True, verbose_name='Nom'),
        ),
    ]
