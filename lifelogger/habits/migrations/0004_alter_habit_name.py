# Generated by Django 4.2 on 2023-05-12 07:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('habits', '0003_alter_habit_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='name',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
    ]
