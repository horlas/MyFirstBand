# Generated by Django 2.1.5 on 2019-02-21 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians', '0018_auto_20190221_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=60, verbose_name='Nom'),
        ),
    ]
