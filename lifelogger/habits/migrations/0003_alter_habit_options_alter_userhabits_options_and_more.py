# Generated by Django 4.2 on 2023-04-25 05:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('habits', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='habit',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='userhabits',
            options={'ordering': ('date',)},
        ),
        migrations.AlterField(
            model_name='userhabits',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
