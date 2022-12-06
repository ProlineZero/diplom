# Generated by Django 4.1.2 on 2022-12-05 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_transmissiontype_delete_car'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('production_start_year', models.IntegerField()),
                ('engine_capacity', models.FloatField()),
                ('engine_power', models.IntegerField()),
                ('popularity', models.IntegerField()),
                ('body_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cars.bodytype')),
                ('engine_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cars.enginetype')),
                ('generation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cars.generation')),
                ('transmission_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cars.transmissiontype')),
            ],
        ),
        migrations.AddConstraint(
            model_name='car',
            constraint=models.CheckConstraint(check=models.Q(('production_start_year__gte', 1850), ('production_start_year__lte', 2022)), name='production_start_year'),
        ),
        migrations.AddConstraint(
            model_name='car',
            constraint=models.CheckConstraint(check=models.Q(('engine_power__gt', 0), ('engine_power__lte', 5000)), name='engine_power'),
        ),
        migrations.AddConstraint(
            model_name='car',
            constraint=models.CheckConstraint(check=models.Q(('engine_capacity__gte', 0), ('engine_capacity__lte', 30)), name='engine_capacity'),
        ),
    ]