# Generated by Django 5.0.6 on 2024-06-10 21:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0009_remove_favorites_car_favorites_cars'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(db_column='rating', default=0)),
                ('description', models.CharField(db_column='description', default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Resolve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(db_column='description', default='', max_length=256)),
                ('is_right', models.BooleanField(db_column='is_right', default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Trouble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(db_column='description', default='', max_length=256)),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='car',
            name='year_end',
        ),
        migrations.RemoveConstraint(
            model_name='car',
            name='year_start',
        ),
        migrations.AddConstraint(
            model_name='car',
            constraint=models.CheckConstraint(check=models.Q(('year_start__gte', 1850), ('year_start__lte', 2025)), name='year_start'),
        ),
        migrations.AddConstraint(
            model_name='car',
            constraint=models.CheckConstraint(check=models.Q(('year_end__gte', 1850), ('year_end__lte', 2024)), name='year_end'),
        ),
        migrations.AddField(
            model_name='master',
            name='cars',
            field=models.ManyToManyField(to='cars.car'),
        ),
        migrations.AddField(
            model_name='master',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resolve',
            name='master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.master'),
        ),
        migrations.AddField(
            model_name='trouble',
            name='car',
            field=models.ForeignKey(db_column='car', on_delete=django.db.models.deletion.CASCADE, to='cars.car'),
        ),
        migrations.AddField(
            model_name='trouble',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resolve',
            name='trouble',
            field=models.ForeignKey(db_column='trouble', on_delete=django.db.models.deletion.CASCADE, to='cars.trouble'),
        ),
    ]