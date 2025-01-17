# Generated by Django 5.1.2 on 2025-01-16 21:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_renovation_work'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='renovation',
            name='work',
        ),
        migrations.AddField(
            model_name='work',
            name='renovation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='renovations', to='main.renovation'),
            preserve_default=False,
        ),
    ]
