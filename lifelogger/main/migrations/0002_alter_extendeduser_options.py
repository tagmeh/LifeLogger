# Generated by Django 4.2 on 2023-04-25 05:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extendeduser',
            options={'ordering': ('date_joined',)},
        ),
    ]
