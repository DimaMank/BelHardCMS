# Generated by Django 2.2.6 on 2019-10-11 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_auto_20191011_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cv',
            name='client_cv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]