# Generated by Django 3.2.4 on 2021-06-29 17:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16, unique=True)),
                ('expiry_month', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('expiry_year', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(2021)])),
            ],
        ),
    ]
