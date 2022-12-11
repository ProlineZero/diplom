# Generated by Django 4.1.2 on 2022-12-09 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0016_drivetype_remove_car_engine_capacity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='back_brakes',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='body_height',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='body_length',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='body_width',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='cylinders_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='cylinders_order',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='front_brakes',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='kwt_power',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='max_speed',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='seats',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='time_to_100',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='torque',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='weight',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='body_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cars.bodytype'),
        ),
    ]