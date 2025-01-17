# Generated by Django 5.1.2 on 2025-01-17 03:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_stageimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.supervisor', verbose_name='Supervisor'),
        ),
        migrations.AlterField(
            model_name='stageimage',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.stage', verbose_name='Stage'),
        ),
        migrations.AlterField(
            model_name='work',
            name='renovation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='work', to='main.renovation', verbose_name='Renovation'),
        ),
    ]
