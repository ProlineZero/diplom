# Generated by Django 4.1.2 on 2022-12-09 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0015_remove_aboba2_car_delete_aboba_delete_aboba2'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriveType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='car',
            name='engine_capacity',
        ),
        migrations.AddConstraint(
            model_name='car',
            constraint=models.CheckConstraint(check=models.Q(('engine_type', 10), models.Q(('engine_capacity__gte', 0), ('engine_capacity__lte', 30)), _connector='OR'), name='engine_capacity'),
        ),
        migrations.AddField(
            model_name='car',
            name='drive_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cars.drivetype'),
        ),
    ]
