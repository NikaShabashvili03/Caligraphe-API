# Generated by Django 5.1.2 on 2025-01-16 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_renovation_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renovation',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.work', unique=True),
        ),
    ]
