# Generated by Django 5.1.2 on 2025-01-16 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_stagetype_stage_type_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Stage_Type',
        ),
        migrations.DeleteModel(
            name='Work_Type',
        ),
    ]
