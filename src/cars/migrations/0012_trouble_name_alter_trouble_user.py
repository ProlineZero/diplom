# Generated by Django 5.0.6 on 2024-06-11 19:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0011_compare'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='trouble',
            name='name',
            field=models.CharField(db_column='name', default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='trouble',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='troubles', to=settings.AUTH_USER_MODEL),
        ),
    ]
