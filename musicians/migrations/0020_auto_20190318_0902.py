# Generated by Django 2.1.7 on 2019-03-18 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians', '0019_auto_20190221_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=60, null=True, unique=True, verbose_name='Nom'),
        ),
    ]