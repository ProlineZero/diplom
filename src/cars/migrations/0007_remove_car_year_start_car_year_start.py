# Generated by Django 4.1.2 on 2022-12-15 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_dbfiller'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='car',
            name='year_start',
        ),
        migrations.AddConstraint(
            model_name='car',
            constraint=models.CheckConstraint(check=models.Q(('year_start__gte', 1850), ('year_start__lte', 2023)), name='year_start'),
        ),
    ]