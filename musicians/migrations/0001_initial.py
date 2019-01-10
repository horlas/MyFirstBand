# Generated by Django 2.1.4 on 2018-12-30 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djangoyearlessdate.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=60)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('dept', models.CharField(blank=True, max_length=5)),
                ('town', models.CharField(blank=True, max_length=60)),
                ('birth_year', djangoyearlessdate.models.YearField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='./media/user_avatar/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]