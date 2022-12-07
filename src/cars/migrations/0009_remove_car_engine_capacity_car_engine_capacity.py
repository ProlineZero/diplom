# Generated by Django 4.1.2 on 2022-12-06 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0008_alter_generation_name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='car',
            name='engine_capacity',
        ),
        migrations.AddConstraint(
            model_name='car',
            constraint=models.CheckConstraint(check=models.Q(('engine_type', 7), models.Q(('engine_capacity__gte', 0), ('engine_capacity__lte', 30)), _connector='OR'), name='engine_capacity'),
        ),
    ]
